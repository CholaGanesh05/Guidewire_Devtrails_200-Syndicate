import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.model_selection import train_test_split
import joblib
import requests
from datetime import datetime, timedelta

print("🌍 Fetching ORIGINAL Real-World Data (Bengaluru Historical Weather)...")
# Bengaluru coordinates
lat = 12.9716
lon = 77.5946

# Get last 30 days of weather to act as our real-world anchor
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
start_str = start_date.strftime('%Y-%m-%d')
end_str = end_date.strftime('%Y-%m-%d')

url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_str}&end_date={end_str}&hourly=temperature_2m,precipitation"
response = requests.get(url)
if response.status_code == 200:
    weather_data = response.json()['hourly']
    df_weather = pd.DataFrame({
        'time': pd.to_datetime(weather_data['time']),
        'temperature_2m': weather_data['temperature_2m'],
        'precipitation': weather_data['precipitation']
    })
    print(f"✅ Successfully fetched {len(df_weather)} hours of real weather data!")
else:
    print("❌ API Error. Falling back to synthetic weather.")
    # Fallback in case of API failure
    times = [start_date + timedelta(hours=i) for i in range(720)]
    df_weather = pd.DataFrame({
        'time': times,
        'temperature_2m': np.random.uniform(20, 35, 720),
        'precipitation': np.random.choice([0, 0, 0, 5, 12, 20], 720)
    })

# Engineer the "Lagged" weather feature to prevent look-ahead bias
df_weather['precip_last_2_hours'] = df_weather['precipitation'].rolling(window=2, closed='left').sum().fillna(0)

print("\n🧬 Generating Synthetic Rider Behavior Profiles...")
num_riders = 500
rider_ids = [f"R_{i}" for i in range(num_riders)]

df_riders = pd.DataFrame({
    'rider_id': rider_ids,
    'inter_order_variance': np.random.uniform(0.1, 5.0, num_riders),
    'rider_tenure_days': np.random.randint(1, 365, num_riders),
    'claims_count': np.random.randint(0, 10, num_riders),
    'trust_score': np.random.randint(20, 100, num_riders),
    'zone_risk_variance': np.random.uniform(1.0, 5.0, num_riders),
    'avg_velocity_kmph': np.random.uniform(15, 60, num_riders) 
})

print("\n🔗 Merging Real Weather + Synthetic Riders -> HYBRID DATASET")
# Generate random trips during this 30-day period
num_trips = 10000
random_rider_ids = np.random.choice(rider_ids, num_trips)
# Randomly sample times from the real weather dataframe
random_times = df_weather['time'].sample(num_trips, replace=True).values

df_trips = pd.DataFrame({
    'rider_id': random_rider_ids,
    'time': random_times
})

# Merge Trip -> Rider Data
df_hybrid = pd.merge(df_trips, df_riders, on='rider_id')
# Merge Trip -> Real Weather Data
df_hybrid = pd.merge(df_hybrid, df_weather, on='time')

df_hybrid['time_of_day'] = df_hybrid['time'].dt.hour

# Engineer Realistic Target Variables (Income Loss is higher when it rains heavily during peak hours)
# Peak hours: 12-14 (Lunch), 19-21 (Dinner)
def calc_income_loss(row):
    peak_multiplier = 2.0 if row['time_of_day'] in [12,13,14,19,20,21] else 1.0
    rain_penalty = row['precip_last_2_hours'] * 15 # Rs lost per mm of rain
    return min(rain_penalty * peak_multiplier, 600) + np.random.normal(0, 10)

df_hybrid['target_income_loss'] = df_hybrid.apply(calc_income_loss, axis=1)

# Premium cost logic (high variance + low trust = higher cost)
df_hybrid['target_loss_cost'] = (df_hybrid['inter_order_variance'] * 5) - (df_hybrid['trust_score'] * 0.2) + 25 + np.random.normal(0, 5)

print(f"✅ Hybrid Dataset Created: {len(df_hybrid)} rows.")

print("\n1. Training XGBoost Premium Model (on Hybrid Features)...")
features_premium = ['inter_order_variance', 'rider_tenure_days', 'claims_count', 'trust_score', 'zone_risk_variance']
premium_model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=4)
premium_model.fit(df_hybrid[features_premium], df_hybrid['target_loss_cost'])
joblib.dump(premium_model, 'premium_model.pkl')
print("✅ Saved premium_model.pkl")

print("\n2. Training Random Forest Income Model (on Real Weather + Synthetic Peaks)...")
features_income = ['time_of_day', 'precip_last_2_hours', 'zone_risk_variance']
income_model = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
income_model.fit(df_hybrid[features_income], df_hybrid['target_income_loss'])
joblib.dump(income_model, 'income_model.pkl')
print("✅ Saved income_model.pkl")

print("\n3. Training Graph/Isolation Fraud Model (Injecting Spoofs)...")
# Inject 3% teleportation anomalies
df_hybrid.loc[df_hybrid.sample(frac=0.03).index, 'avg_velocity_kmph'] = np.random.uniform(150, 400, int(num_trips*0.03))
features_fraud = ['avg_velocity_kmph', 'inter_order_variance']
fraud_model = IsolationForest(n_estimators=100, contamination=0.03, random_state=42)
fraud_model.fit(df_hybrid[features_fraud])
joblib.dump(fraud_model, 'fraud_model.pkl')
print("✅ Saved fraud_model.pkl")

print("\n🎉 SUCCESS! Hybrid models dynamically generated.")
