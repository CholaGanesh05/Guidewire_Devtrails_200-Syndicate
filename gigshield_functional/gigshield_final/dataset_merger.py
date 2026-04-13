"""
dataset_merger.py
ArthSahay - Hybrid Real-World Dataset Merger Pipeline

This module is designed to merge open-source Kaggle delivery/rideshare data
with actual historical weather data from Open-Meteo. 

Key features:
1. API Caching (SQLite) to prevent hitting rate limits during bulk data fetching.
2. Prevention of Look-Ahead Bias by ensuring weather merges on `order_placed_time`
   and computes rolling lagged features (e.g. `precip_last_2_hours`).
3. User Variance profiling computation for Premium prediction.
"""

import pandas as pd
import requests
import sqlite3
import json
import time
from datetime import datetime, timedelta

# Create an SQLite Cache connection
CACHE_DB = "weather_api_cache.sqlite"
conn = sqlite3.connect(CACHE_DB)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_cache (
        lat REAL,
        lon REAL,
        date TEXT,
        response_json TEXT,
        PRIMARY KEY (lat, lon, date)
    )
''')
conn.commit()


def fetch_historical_weather_daily(lat, lon, date_str):
    """
    Fetches hourly historical weather data for a specific day from Open-Meteo.
    Uses SQLite to cache responses and avoid rate limits.
    """
    # Check Cache
    cursor.execute('SELECT response_json FROM weather_cache WHERE lat=? AND lon=? AND date=?', (lat, lon, date_str))
    row = cursor.fetchone()
    
    if row:
        return json.loads(row[0])
    
    # Not in cache, hit API
    url = f"https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": date_str,
        "end_date": date_str,
        "hourly": "temperature_2m,precipitation,rain,wind_speed_10m"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        cursor.execute("INSERT INTO weather_cache (lat, lon, date, response_json) VALUES (?, ?, ?, ?)", 
                       (lat, lon, date_str, json.dumps(data)))
        conn.commit()
        time.sleep(0.1) # Small delay to respect free-tier rate limits
        return data
    else:
        print(f"Failed to fetch {date_str} for {lat},{lon}: {response.status_code}")
        return None

def engineer_weather_lags(weather_df):
    """
    Prevent Look-Ahead Bias: Create lag features so the model only knows 
    what happened BEFORE the order was placed.
    """
    # Sort chronologically
    weather_df = weather_df.sort_values(by="time").reset_index(drop=True)
    
    # Create a 2-hour rolling sum of precipitation leading up to the current hour
    # Use 'closed=left' to ensure we only look at precipitation BEFORE the current hour
    weather_df['precip_last_2_hours'] = weather_df['precipitation'].rolling(window=2, closed='left').sum()
    
    # Fill NaN for the first 2 hours
    weather_df['precip_last_2_hours'] = weather_df['precip_last_2_hours'].fillna(0)
    
    return weather_df

def process_and_merge_delivery_dataset(kaggle_csv_path, default_lat=12.9716, default_lon=77.5946):
    """
    Loads Kaggle Delivery Data, merges with weather while respecting causality.
    """
    print(f"Loading Kaggle dataset: {kaggle_csv_path}")
    # Simulate loading Kaggle Dataset
    # df = pd.read_csv(kaggle_csv_path)
    
    # For demonstration, creating a mock dataframe representing Kaggle data structure
    df = pd.DataFrame({
        "order_id": [101, 102, 103],
        "rider_id": ["R_001", "R_001", "R_002"],
        "order_placed_time": ["2023-07-15 14:00", "2023-07-15 15:30", "2023-07-15 20:00"],
        "delivery_time_mins": [35, 45, 60]
    })
    
    df['order_placed_time'] = pd.to_datetime(df['order_placed_time'])
    df['date_str'] = df['order_placed_time'].dt.strftime('%Y-%m-%d')
    df['hour'] = df['order_placed_time'].dt.strftime('%Y-%m-%dT%H:00')
    
    unique_dates = df['date_str'].unique()
    
    all_weather_data = []
    print("Fetching weather integrations...")
    for date_str in unique_dates:
        w_data = fetch_historical_weather_daily(default_lat, default_lon, date_str)
        if w_data and 'hourly' in w_data:
            hourly = w_data['hourly']
            temp_df = pd.DataFrame({
                "time": hourly["time"],
                "temperature": hourly["temperature_2m"],
                "precipitation": hourly["precipitation"]
            })
            all_weather_data.append(temp_df)
            
    if all_weather_data:
        weather_df = pd.concat(all_weather_data)
        
        # Apply lag engineering BEFORE merging
        weather_df = engineer_weather_lags(weather_df)
        
        # Merge on the hour the order was PLACED (no look-ahead to delivery_time)
        merged_df = pd.merge(df, weather_df, left_on="hour", right_on="time", how="left")
        return merged_df
    
    return df

def generate_rider_variance_profile(df):
    """
    Extracts the 'loyalty and predictability' variance per rider 
    to be used by the Premium Model.
    """
    df = df.sort_values(by=["rider_id", "order_placed_time"])
    df['time_since_last_order'] = df.groupby('rider_id')['order_placed_time'].diff().dt.total_seconds() / 3600
    
    variance_profile = df.groupby('rider_id').agg(
        total_orders=('order_id', 'count'),
        avg_inter_order_time_hrs=('time_since_last_order', 'mean'),
        inter_order_variance=('time_since_last_order', 'var')
    ).reset_index()
    
    # Fill variance NaNs for riders with < 2 orders
    variance_profile['inter_order_variance'] = variance_profile['inter_order_variance'].fillna(0)
    
    return variance_profile

if __name__ == "__main__":
    print("=== ArthSahay Hybrid Dataset Merger ===")
    # 1. Provide the path to the downloaded Kaggle dataset
    csv_path = "mock_kaggle_data.csv" 
    
    # 2. Merge data cleanly with API caching and lagged weather
    final_hybrid_data = process_and_merge_delivery_dataset(csv_path)
    print("\nSample Merged Data (Causal - No Look-ahead Bias):")
    print(final_hybrid_data.head())
    
    # 3. Compute Rider Profiles for the XGBoost Premium Model
    rider_profiles = generate_rider_variance_profile(final_hybrid_data)
    print("\nRider Variance Profiles:")
    print(rider_profiles.head())
    
    # final_hybrid_data.to_csv("processed_hybrid_training_data.csv", index=False)
