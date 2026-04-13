"""
ArthSahay – AI-Powered Parametric Income Insurance
Full Functional Flask Application
"""

import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random
import math
import time
import json
from datetime import datetime, timedelta
import joblib
try:
    import pandas as pd
except ImportError:
    pd = None
import requests
from agent_engine import synthesize_agent_rationale

try:
    premium_model = joblib.load('premium_model.pkl')
    income_model  = joblib.load('income_model.pkl')
    fraud_model   = joblib.load('fraud_model.pkl')
    print("✅ ML Models loaded into ArthSahay API successfully.")
except Exception as e:
    premium_model, income_model, fraud_model = None, None, None
    print("⚠️ ML Models missing. Fallback to deterministic formulas.", e)

app = Flask(__name__)
app.secret_key = "arthsahay-secret-2026"

from flask_sqlalchemy import SQLAlchemy

# ─────────────────────────────────────────────────────────────────
# DATABASE STORE
# ─────────────────────────────────────────────────────────────────

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arthsahay.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class RiderModel(db.Model):
    phone = db.Column(db.String(20), primary_key=True)
    data = db.Column(db.Text, nullable=False)

class PayoutModel(db.Model):
    phone = db.Column(db.String(20), primary_key=True)
    data = db.Column(db.Text, nullable=False)

class PremiumPaymentModel(db.Model):
    phone = db.Column(db.String(20), primary_key=True)
    data = db.Column(db.Text, nullable=False)

class PersistentDict:
    def __init__(self, model):
        self.model = model
    def get(self, key, default=None):
        record = self.model.query.get(str(key))
        return json.loads(record.data) if record else default
    def __getitem__(self, key):
        record = self.model.query.get(str(key))
        if record: return json.loads(record.data)
        raise KeyError(key)
    def __setitem__(self, key, value):
        record = self.model.query.get(str(key))
        if not record:
            record = self.model(phone=str(key), data=json.dumps(value))
            db.session.add(record)
        else:
            record.data = json.dumps(value)
        db.session.commit()
    def __contains__(self, key):
        return self.model.query.get(str(key)) is not None
    def values(self):
        return [json.loads(r.data) for r in self.model.query.all()]
    def items(self):
        return [(r.phone, json.loads(r.data)) for r in self.model.query.all()]
    def keys(self):
        return [r.phone for r in self.model.query.all()]
    def __iter__(self):
        return iter([r.phone for r in self.model.query.all()])
    def __len__(self):
        return self.model.query.count()
    def __bool__(self):
        return self.__len__() > 0

riders = PersistentDict(RiderModel)
payouts = PersistentDict(PayoutModel)
premium_payments = PersistentDict(PremiumPaymentModel)
active_events = {}

with app.app_context():
    db.create_all()

# ─────────────────────────────────────────────────────────────────
# ZONE BASELINES (90-day historical simulated data)
# μ = mean, σ = std deviation for each metric
# ─────────────────────────────────────────────────────────────────

ZONE_BASELINES = {
    "Koramangala, Bengaluru": {
        "rain_mm_hr": {"mu": 22, "sigma": 8},
        "aqi":        {"mu": 120, "sigma": 30},
        "temp_c":     {"mu": 26, "sigma": 3},
        "traffic":    {"mu": 55, "sigma": 15},
        "city": "Bengaluru"
    },
    "Banjara Hills, Hyderabad": {
        "rain_mm_hr": {"mu": 18, "sigma": 6},
        "aqi":        {"mu": 130, "sigma": 35},
        "temp_c":     {"mu": 30, "sigma": 4},
        "traffic":    {"mu": 60, "sigma": 18},
        "city": "Hyderabad"
    },
    "Anna Nagar, Chennai": {
        "rain_mm_hr": {"mu": 25, "sigma": 10},
        "aqi":        {"mu": 110, "sigma": 28},
        "temp_c":     {"mu": 36, "sigma": 3},
        "traffic":    {"mu": 65, "sigma": 20},
        "city": "Chennai"
    },
    "Vaishali Nagar, Jaipur": {
        "rain_mm_hr": {"mu": 8, "sigma": 4},
        "aqi":        {"mu": 160, "sigma": 40},
        "temp_c":     {"mu": 35, "sigma": 6},
        "traffic":    {"mu": 45, "sigma": 12},
        "city": "Jaipur"
    },
    "Andheri West, Mumbai": {
        "rain_mm_hr": {"mu": 35, "sigma": 15},
        "aqi":        {"mu": 140, "sigma": 35},
        "temp_c":     {"mu": 30, "sigma": 3},
        "traffic":    {"mu": 75, "sigma": 20},
        "city": "Mumbai"
    },
    "Malleshwaram, Bengaluru": {
        "rain_mm_hr": {"mu": 20, "sigma": 7},
        "aqi":        {"mu": 115, "sigma": 25},
        "temp_c":     {"mu": 27, "sigma": 3},
        "traffic":    {"mu": 58, "sigma": 16},
        "city": "Bengaluru"
    },
}

DISRUPTION_LEVEL_CONFIG = {
    0: {"label": "L0 – Normal",    "pct": 0,    "color": "#27ae60", "desc": "Within zone baseline"},
    1: {"label": "L1 – Mild",      "pct": 0.25, "color": "#f39c12", "desc": "Mild deviation (~25% payout)"},
    2: {"label": "L2 – Moderate",  "pct": 0.50, "color": "#e67e22", "desc": "Moderate deviation (~50% payout)"},
    3: {"label": "L3 – High",      "pct": 0.75, "color": "#e74c3c", "desc": "High deviation (~75% payout)"},
    4: {"label": "L4 – Shutdown",  "pct": 1.00, "color": "#8e44ad", "desc": "Complete shutdown (100% payout)"},
}

PLATFORMS = ["Swiggy", "Zomato", "Both"]
ZONES = list(ZONE_BASELINES.keys())


# ─────────────────────────────────────────────────────────────────
# CORE LOGIC FUNCTIONS
# ─────────────────────────────────────────────────────────────────

def compute_deviation(value, mu, sigma):
    """Returns deviation percentage from baseline mean (in sigmas * 100)."""
    if sigma == 0:
        return 0
    return ((value - mu) / sigma)  # z-score

def deviation_to_level(z_score):
    """Maps z-score deviation to disruption level L0–L4."""
    if z_score < 1.0:    return 0
    elif z_score < 1.5:  return 1
    elif z_score < 2.0:  return 2
    elif z_score < 2.5:  return 3
    else:                return 4

def fuse_disruption_levels(*levels):
    """Multi-trigger fusion: max level, with upgrade if 2+ signals at L2+."""
    max_lv = max(levels)
    high_signals = sum(1 for l in levels if l >= 2)
    if high_signals >= 2 and max_lv < 4:
        return min(max_lv + 1, 4)
    return max_lv

def calculate_dynamic_premium(zone, daily_earnings, trust_score, season="normal"):
    """
    Dynamic weekly premium model predicting expected loss.
    Uses XGBoost premium_model.pkl if available, else falls back to local math.
    """
    if premium_model is not None:
        # Formulate feature vector for XGBoost inference
        # In a real app, rider_tenure_days and inter_order_variance come from DB.
        rider_tenure = max(1, trust_score // 2)
        df_pred = pd.DataFrame([{
            'inter_order_variance': 2.5,  # Realistically retrieved from Rider profile
            'rider_tenure_days': rider_tenure,
            'claims_count': 0,            # Would be fetched from DB
            'trust_score': trust_score,
            'zone_risk_variance': 3.0     # Mock for Zone baseline variance
        }])
        ml_premium = float(premium_model.predict(df_pred)[0])
        return round(max(15, min(ml_premium, 60)), 2)
    
    # ── Fallback Deterministic Logic ──
    baseline = ZONE_BASELINES.get(zone, list(ZONE_BASELINES.values())[0])
    weekly_earnings = daily_earnings * 6
    base = weekly_earnings * 0.025
    rain_risk = baseline["rain_mm_hr"]["sigma"] / 10
    aqi_risk  = baseline["aqi"]["sigma"] / 50
    zone_modifier = (rain_risk + aqi_risk) / 2
    seasonal = {"monsoon": 1.3, "summer": 1.1, "normal": 1.0, "winter": 0.9}.get(season, 1.0)
    
    trust_discount = 0
    if trust_score >= 71:   trust_discount = 0.20
    elif trust_score >= 41: trust_discount = 0.10
    
    premium = base * (1 + zone_modifier * 0.3) * seasonal * (1 - trust_discount)
    return round(max(15, min(premium, 40)), 2)

def calculate_payout(daily_earnings, disruption_level, active_hours=8, disruption_hours=4):
    """
    Payout is determined by the Random Forest Model using temporal impact.
    """
    if disruption_level == 0:
        return 0
        
    if income_model is not None:
        # Form feature vector representing current temporal and local severity
        current_hour = datetime.now().hour
        # Map L1-L4 to relative precipitation for the model feature
        precip_vector = {1: 15, 2: 30, 3: 45, 4: 60}.get(disruption_level, 10)
        
        df_pred = pd.DataFrame([{
            'time_of_day': current_hour,
            'precip_last_2_hours': precip_vector,
            'zone_risk_variance': 3.0
        }])
        ml_payout = float(income_model.predict(df_pred)[0])
        # Add tiny variance adjustment proportionally for higher daily earners if needed
        # but the RandomForest dictates the core loss value
        ml_payout = ml_payout * (daily_earnings / 800.0) # Scaled to their basic standard 
        return round(min(ml_payout, 600), 2)

    # ── Fallback Deterministic Logic ──
    hourly_rate = daily_earnings / active_hours
    pct = DISRUPTION_LEVEL_CONFIG[disruption_level]["pct"]
    payout = disruption_hours * hourly_rate * pct
    return round(min(payout, 600), 2)

def compute_trust_score(rider):
    """
    Trust score based on:
    - Days enrolled (longevity)
    - Payout claim frequency vs disruption events
    - GPS consistency flags
    """
    base = 50
    days_enrolled = max(rider.get("days_enrolled", 1), 1)
    claims_count  = rider.get("claims_count", 0)
    fraud_flags   = rider.get("fraud_flags", 0)

    longevity_bonus = min(days_enrolled * 0.5, 20)
    fraud_penalty   = fraud_flags * 10
    claim_ratio_ok  = 1 if claims_count < 3 else 0  # +5 if reasonable claim frequency

    score = base + longevity_bonus - fraud_penalty + (claim_ratio_ok * 5)
    return max(0, min(int(score), 100))

def get_trust_tier(score):
    if score >= 71:  return {"name": "Gold",   "emoji": "🥇", "payout_bonus": 0.25}
    elif score >= 41: return {"name": "Silver", "emoji": "🥈", "payout_bonus": 0.10}
    else:             return {"name": "Bronze", "emoji": "🥉", "payout_bonus": 0.00}

def simulate_current_conditions(rider_or_zone):
    """
    Dynamically fetches real-world physical meteorology for the rider's active location.
    Maps the string zone to actual terrestrial Lat/Lon and hits Open-Meteo live API.
    """
    zone = rider_or_zone.get("zone", "Unknown") if isinstance(rider_or_zone, dict) else rider_or_zone
    baseline = ZONE_BASELINES.get(zone, list(ZONE_BASELINES.values())[0])
    
    # ── Actual Physical Geographic Mapping ──
    ZONE_COORDS = {
        "Koramangala, Bengaluru": (12.9279, 77.6271),
        "Banjara Hills, Hyderabad": (17.4156, 78.4419),
        "Anna Nagar, Chennai": (13.0837, 80.2117),
        "Bandra West, Mumbai": (19.0596, 72.8295),
        "Connaught Place, Delhi": (28.6304, 77.2177)
    }
    
    # Extract dynamic GPS if captured organically by OpenStreetMap Javascript, otherwise fallback
    lat = rider_or_zone.get("lat") if isinstance(rider_or_zone, dict) else None
    lon = rider_or_zone.get("lon") if isinstance(rider_or_zone, dict) else None
    
    if not lat or not lon:
        lat, lon = ZONE_COORDS.get(zone, (12.9716, 77.5946))
    
    # Time-seeded randomness solely for Traffic & AQI variance (since Open-Meteo doesn't have live traffic)
    seed = int(time.time() / 600) + hash(zone) % 1000
    rng = random.Random(seed)
    
    try:
        # Dynamic Real-World Environmental Fetching directly into the physics engine
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=precipitation,temperature_2m"
        resp = requests.get(url, timeout=4).json()
        current = resp.get("current", {})
        
        rain = float(current.get("precipitation", 0.0))
        temp = float(current.get("temperature_2m", 25.0))
        print(f"🌍 Live GPS sync for {zone} ({lat}, {lon}) - Rain: {rain}mm/h, Temp: {temp}C")
    except Exception as e:
        print(f"⚠️ Weather API Error ({e}). Falling back to algorithmic approximation.")
        # Local fallback if the rider goes offline or API rate-limited
        rain = max(0, round(baseline["rain_mm_hr"]["mu"] + baseline["rain_mm_hr"]["sigma"] * rng.gauss(0, 0.5), 1))
        temp = round(baseline["temp_c"]["mu"] + baseline["temp_c"]["sigma"] * rng.gauss(0, 0.5), 1)

    # Traffic and AQI stay bounded algorithmic deviations based on historical baselines
    aqi = max(50, round(baseline["aqi"]["mu"] + baseline["aqi"]["sigma"] * rng.gauss(0, 0.5), 1))
    traffic = min(100, max(0, round(baseline["traffic"]["mu"] + baseline["traffic"]["sigma"] * rng.gauss(0, 1.0), 1)))

    rain_z   = compute_deviation(rain,    baseline["rain_mm_hr"]["mu"], baseline["rain_mm_hr"]["sigma"])
    aqi_z    = compute_deviation(aqi,     baseline["aqi"]["mu"],        baseline["aqi"]["sigma"])
    temp_z   = compute_deviation(temp,    baseline["temp_c"]["mu"],     baseline["temp_c"]["sigma"])
    traffic_z = compute_deviation(traffic, baseline["traffic"]["mu"],   baseline["traffic"]["sigma"])

    rain_lv    = deviation_to_level(max(rain_z, 0))
    aqi_lv     = deviation_to_level(max(aqi_z, 0))
    temp_lv    = deviation_to_level(max(temp_z, 0))
    traffic_lv = deviation_to_level(max(traffic_z, 0))

    fused_level = fuse_disruption_levels(rain_lv, aqi_lv, temp_lv, traffic_lv)

    # Demand drop (correlated with disruption)
    demand_drop = min(round(fused_level * 18 + rng.uniform(-5, 5)), 80)

    return {
        "rain_mm_hr":  rain,
        "aqi":         aqi,
        "temp_c":      temp,
        "traffic_pct": traffic,
        "rain_deviation_pct":    round(rain_z * 100, 1),
        "aqi_deviation_pct":     round(aqi_z * 100, 1),
        "temp_deviation_pct":    round(temp_z * 100, 1),
        "traffic_deviation_pct": round(traffic_z * 100, 1),
        "rain_level":    rain_lv,
        "aqi_level":     aqi_lv,
        "temp_level":    temp_lv,
        "traffic_level": traffic_lv,
        "fused_level":   fused_level,
        "fused_label":   DISRUPTION_LEVEL_CONFIG[fused_level]["label"],
        "fused_color":   DISRUPTION_LEVEL_CONFIG[fused_level]["color"],
        "demand_drop_pct": demand_drop,
        "baseline": {
            "rain_mu":    baseline["rain_mm_hr"]["mu"],
            "aqi_mu":     baseline["aqi"]["mu"],
            "temp_mu":    baseline["temp_c"]["mu"],
            "traffic_mu": baseline["traffic"]["mu"],
        }
    }

def fraud_check(rider, zone, conditions):
    """Run automated fraud validation checks."""
    checks = []
    
    # GPS presence check (simulated: 95% pass rate)
    gps_ok = random.random() > 0.05
    checks.append({"name": "GPS in disruption zone", "pass": gps_ok})

    # Demand drop confirmation
    demand_ok = conditions["demand_drop_pct"] >= 20
    checks.append({"name": f"Order volume drop {conditions['demand_drop_pct']}%", "pass": demand_ok})

    # GPS spoof detection (velocity anomaly via Isolation Forest)
    if fraud_model is not None:
        # We simulate fetching the rider's recent velocity track
        # A normal ping is 15-40 km/h. We occasionaly simulate them acting weird 
        # (if spoofing happened) but for the API demo, we assume they are genuine mostly.
        simulated_velocity = random.uniform(15, 40) 
        df_fraud = pd.DataFrame([{
            'avg_velocity_kmph': simulated_velocity,
            'inter_order_variance': 2.0
        }])
        pred = fraud_model.predict(df_fraud)[0]
        spoof_ok = (pred == 1) # 1 is Normal, -1 is anomaly
    else:
        spoof_ok = random.random() > 0.02
        
    checks.append({"name": "No GPS spoof detected", "pass": bool(spoof_ok)})

    # Duplicate claim today
    today = datetime.now().strftime("%Y-%m-%d")
    phone = rider.get("phone", "")
    today_payouts = [p for p in payouts.get(phone, []) if p["date"] == today]
    no_prior = len(today_payouts) == 0
    checks.append({"name": "No prior claim today", "pass": no_prior})

    all_pass = all(c["pass"] for c in checks)
    return checks, all_pass

def generate_payout_history(phone):
    """Generate realistic payout history for a rider."""
    history = payouts.get(phone, [])
    return history[-10:]  # last 10 records


# ─────────────────────────────────────────────────────────────────
# ROUTES – Pages
# ─────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    rider = None
    if "phone" in session:
        rider = riders.get(session["phone"])
    return render_template("index.html", rider=rider, zones=ZONES)

@app.route("/onboard", methods=["GET", "POST"])
def onboard():
    if request.method == "POST":
        data = request.form
        phone = data.get("phone", "").strip()
        name  = data.get("name", "").strip()
        zone  = data.get("zone", "").strip()
        platform = data.get("platform", "Swiggy").strip()
        try:
            daily_earnings = float(data.get("daily_earnings", 800))
        except:
            daily_earnings = 800

        if not phone or not name or not zone:
            return render_template("onboard.html", zones=ZONES, platforms=PLATFORMS,
                                   error="Please fill all fields correctly.")

        trust_score = 50  # initial
        premium = calculate_dynamic_premium(zone, daily_earnings, trust_score)

        riders[phone] = {
            "phone":          phone,
            "name":           name,
            "zone":           zone,
            "platform":       platform,
            "daily_earnings": daily_earnings,
            "trust_score":    trust_score,
            "premium":        premium,
            "lat":            data.get("sys_lat", ""),
            "lon":            data.get("sys_lon", ""),
            "enrolled_at":    datetime.now().isoformat(),
            "days_enrolled":  1,
            "claims_count":   0,
            "fraud_flags":    0,
            "active":         True,
        }
        payouts[phone] = []
        session["phone"] = phone
        return redirect(url_for("dashboard"))

    return render_template("onboard.html", zones=ZONES, platforms=PLATFORMS)

@app.route("/dashboard")
def dashboard():
    if "phone" not in session:
        return redirect(url_for("onboard"))
    rider = riders.get(session["phone"])
    if not rider:
        return redirect(url_for("onboard"))

    conditions = simulate_current_conditions(rider)
    trust_score = compute_trust_score(rider)
    trust_tier  = get_trust_tier(trust_score)
    rider["trust_score"] = trust_score

    # Weekly premium (refreshed)
    premium = calculate_dynamic_premium(rider["zone"], rider["daily_earnings"], trust_score)
    rider["premium"] = premium

    # Estimated payout if disruption triggered now
    est_payout = calculate_payout(rider["daily_earnings"], conditions["fused_level"])
    history = generate_payout_history(session["phone"])

    return render_template("dashboard.html",
                           rider=rider,
                           conditions=conditions,
                           trust_tier=trust_tier,
                           est_payout=est_payout,
                           history=history,
                           disruption_config=DISRUPTION_LEVEL_CONFIG)

@app.route("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html")

@app.route("/coverage")
def coverage():
    return render_template("coverage.html",
                           disruption_config=DISRUPTION_LEVEL_CONFIG)

@app.route("/technology")
def technology():
    return render_template("technology.html")

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ─────────────────────────────────────────────────────────────────
# API ENDPOINTS – JSON (called by frontend JS)
# ─────────────────────────────────────────────────────────────────

@app.route("/api/conditions/<path:zone>")
def api_conditions(zone):
    """Real-time zone conditions API. Works for both known and GPS-detected zones."""
    import urllib.parse
    zone = urllib.parse.unquote(zone)
    # Use zone string as-is; simulate_current_conditions handles unknown zones gracefully.
    return jsonify(simulate_current_conditions({"zone": zone}))

@app.route("/api/premium-preview")
def api_premium_preview():
    """Calculate premium preview without saving."""
    zone = request.args.get("zone", ZONES[0])
    try:
        earnings = float(request.args.get("earnings", 800))
    except:
        earnings = 800
    trust = int(request.args.get("trust", 50))
    season = request.args.get("season", "normal")
    premium = calculate_dynamic_premium(zone, earnings, trust, season)
    weekly = earnings * 6
    return jsonify({
        "premium": premium,
        "weekly_earnings": weekly,
        "coverage_ratio": round(premium / weekly * 100, 2),
        "max_daily_payout": 600,
        "trust_tier": get_trust_tier(trust)["name"]
    })

@app.route("/api/trigger-disruption", methods=["POST"])
def api_trigger_disruption():
    """
    Trigger a disruption event for the current rider.
    Runs full validation pipeline and calculates payout.
    """
    if "phone" not in session:
        return jsonify({"error": "Not logged in"}), 401

    phone = session["phone"]
    rider = riders.get(phone)
    if not rider:
        return jsonify({"error": "Rider not found"}), 404

    data = request.get_json() or {}
    # Allow manual override of conditions for simulation
    intensity = data.get("intensity", "auto")  # auto, mild, moderate, high, extreme

    zone = rider["zone"]
    conditions = simulate_current_conditions(rider)

    # Override intensity if requested
    if intensity == "mild":
        conditions["fused_level"] = 1
    elif intensity == "moderate":
        conditions["fused_level"] = 2
    elif intensity == "high":
        conditions["fused_level"] = 3
    elif intensity == "extreme":
        conditions["fused_level"] = 4

    if conditions["fused_level"] == 0:
        return jsonify({
            "status": "no_disruption",
            "message": "Current conditions are within baseline. No payout triggered.",
            "conditions": conditions
        })

    # Run fraud checks
    fraud_checks_result, fraud_ok = fraud_check(rider, zone, conditions)

    if not fraud_ok:
        rider["fraud_flags"] = rider.get("fraud_flags", 0) + 1
        riders[phone] = rider
        return jsonify({
            "status": "fraud_blocked",
            "message": "Validation failed. Payout blocked.",
            "fraud_checks": fraud_checks_result,
            "conditions": conditions
        })

    # Calculate payout
    level = conditions["fused_level"]
    disruption_hours = {1: 2, 2: 3, 3: 4, 4: 6}.get(level, 4)
    payout = calculate_payout(rider["daily_earnings"], level, disruption_hours=disruption_hours)

    # Trust tier bonus
    trust_tier = get_trust_tier(compute_trust_score(rider))
    payout = round(payout * (1 + trust_tier["payout_bonus"]), 2)
    payout = min(payout, 600)

    # Record payout
    record = {
        "date":        datetime.now().strftime("%Y-%m-%d"),
        "time":        datetime.now().strftime("%H:%M"),
        "zone":        zone,
        "level":       level,
        "level_label": DISRUPTION_LEVEL_CONFIG[level]["label"],
        "payout":      payout,
        "disruption_hours": disruption_hours,
        "conditions":  {
            "rain": conditions["rain_mm_hr"],
            "aqi":  conditions["aqi"],
            "temp": conditions["temp_c"],
        }
    }
    plist = payouts.get(phone, [])
    plist.append(record)
    payouts[phone] = plist
    
    rider["claims_count"] = rider.get("claims_count", 0) + 1
    riders[phone] = rider

    # Call LangChain Agent Orchestrator to generate validation paragraph!
    rationale = synthesize_agent_rationale(zone, payout, fraud_ok, conditions["fused_level"])

    return jsonify({
        "status": "payout_approved",
        "payout": payout,
        "level": level,
        "level_label": DISRUPTION_LEVEL_CONFIG[level]["label"],
        "level_color": DISRUPTION_LEVEL_CONFIG[level]["color"],
        "disruption_hours": disruption_hours,
        "fraud_checks": fraud_checks_result,
        "conditions": conditions,
        "agent_rationale": rationale,
        "whatsapp_msg": (
            f"\u26a0\ufe0f ArthSahay Alert \u2014 {DISRUPTION_LEVEL_CONFIG[level]['label']} disruption detected in {zone}.\n"
            f"\u20b9{payout:.0f} triggered for {disruption_hours} hours of income loss.\n"
            f"Trust tier bonus applied: {trust_tier['name']} {trust_tier['emoji']}\n"
            f"UPI processing within 24 hours. Stay safe! \ud83d\udee1\ufe0f"
        ),
        "upi_processing_time": "Within 24 hours"
    })

@app.route("/api/payout-history")
def api_payout_history():
    if "phone" not in session:
        return jsonify([])
    phone = session["phone"]
    return jsonify(generate_payout_history(phone))

@app.route("/api/zone-baselines")
def api_zone_baselines():
    """Return baseline data for all zones (for comparison)."""
    result = {}
    for zone, data in ZONE_BASELINES.items():
        result[zone] = {
            "city": data["city"],
            "rain_baseline": data["rain_mm_hr"]["mu"],
            "aqi_baseline":  data["aqi"]["mu"],
            "temp_baseline": data["temp_c"]["mu"],
        }
    return jsonify(result)

@app.route("/api/rider-profile")
def api_rider_profile():
    if "phone" not in session:
        return jsonify({"error": "Not logged in"}), 401
    phone = session["phone"]
    rider = riders.get(phone, {})
    trust_score = compute_trust_score(rider)
    tier = get_trust_tier(trust_score)
    return jsonify({
        **rider,
        "trust_score": trust_score,
        "trust_tier": tier["name"],
        "trust_emoji": tier["emoji"],
        "total_payouts": sum(p["payout"] for p in payouts.get(phone, [])),
        "payout_count": len(payouts.get(phone, [])),
    })

@app.route("/api/simulate-scenario")
def api_simulate_scenario():
    """
    Simulate a complete scenario without a logged-in rider.
    Used on the How It Works page.
    """
    zone = request.args.get("zone", "Koramangala, Bengaluru")
    try:
        earnings = float(request.args.get("earnings", 800))
    except:
        earnings = 800

    conditions = simulate_current_conditions(zone)
    level = conditions["fused_level"]
    payout = calculate_payout(earnings, level)
    premium = calculate_dynamic_premium(zone, earnings, 65)

    return jsonify({
        "zone": zone,
        "conditions": conditions,
        "disruption_level": level,
        "level_label": DISRUPTION_LEVEL_CONFIG[level]["label"],
        "level_color": DISRUPTION_LEVEL_CONFIG[level]["color"],
        "estimated_payout": payout,
        "weekly_premium": premium,
        "hourly_rate": round(earnings / 8, 2),
        "disruption_hours": {1: 2, 2: 3, 3: 4, 4: 6}.get(level, 0),
    })


# ─────────────────────────────────────────────────────────────────
# PREMIUM PAYMENT SIMULATION
# ─────────────────────────────────────────────────────────────────


@app.route("/api/pay-premium", methods=["POST"])
def api_pay_premium():
    """Simulate UPI premium payment. Marks policy as paid for the week."""
    if "phone" not in session:
        return jsonify({"error": "Not logged in"}), 401
    phone = session["phone"]
    rider = riders.get(phone)
    if not rider:
        return jsonify({"error": "Rider not found"}), 404

    premium = rider.get("premium", 22)
    # Simulate UPI transaction
    txn_id = f"GS{int(time.time())}{random.randint(100,999)}"
    record = {
        "txn_id":    txn_id,
        "amount":    premium,
        "date":      datetime.now().strftime("%Y-%m-%d"),
        "time":      datetime.now().strftime("%H:%M"),
        "method":    "UPI",
        "status":    "SUCCESS",
        "week_of":   datetime.now().strftime("%W/%Y"),
    }
    plist = premium_payments.get(phone, [])
    plist.append(record)
    premium_payments[phone] = plist

    # Update trust score (consistent payer = +5)
    rider["days_enrolled"] = rider.get("days_enrolled", 1) + 7
    rider["trust_score"] = compute_trust_score(rider)
    riders[phone] = rider

    return jsonify({
        "status":    "success",
        "txn_id":    txn_id,
        "amount":    premium,
        "message":   f"₹{premium} paid. Policy active for next 7 days. TXN: {txn_id}",
        "new_trust": rider["trust_score"],
        "new_tier":  get_trust_tier(rider["trust_score"])["name"]
    })

@app.route("/api/payment-history")
def api_payment_history():
    if "phone" not in session:
        return jsonify([])
    return jsonify(premium_payments.get(session["phone"], []))


# ─────────────────────────────────────────────────────────────────
# INSURER / ADMIN CONSOLE
# ─────────────────────────────────────────────────────────────────

@app.route("/admin")
def admin():
    """Insurer console — aggregate view of all riders, zones, payouts."""
    # Seed demo data if no riders yet
    if not riders:
        _seed_demo_data()
    return render_template("admin.html")

def _seed_demo_data():
    """Populate demo riders and payout history for the admin console."""
    demo_riders = [
        ("9876543210", "Ravi Kumar",    "Koramangala, Bengaluru",    "Swiggy", 800),
        ("9123456789", "Priya Sharma",  "Banjara Hills, Hyderabad",  "Zomato", 950),
        ("9988776655", "Arjun Nair",    "Anna Nagar, Chennai",       "Both",   720),
        ("9001234567", "Sunita Patel",  "Vaishali Nagar, Jaipur",    "Swiggy", 680),
        ("9871112233", "Karan Mehta",   "Andheri West, Mumbai",      "Zomato", 1100),
        ("9765432109", "Deepa Rao",     "Malleshwaram, Bengaluru",   "Swiggy", 850),
        ("9654321098", "Suresh Pillai", "Koramangala, Bengaluru",    "Zomato", 780),
        ("9543210987", "Meena Joseph",  "Anna Nagar, Chennai",       "Both",   660),
    ]
    rng = random.Random(42)
    for phone, name, zone, platform, earnings in demo_riders:
        if phone in riders:
            continue
        days = rng.randint(5, 45)
        claims = rng.randint(0, 4)
        ts = rng.randint(40, 90)
        premium = calculate_dynamic_premium(zone, earnings, ts)
        riders[phone] = {
            "phone": phone, "name": name, "zone": zone,
            "platform": platform, "daily_earnings": earnings,
            "trust_score": ts, "premium": premium,
            "enrolled_at": (datetime.now() - timedelta(days=days)).isoformat(),
            "days_enrolled": days, "claims_count": claims,
            "fraud_flags": 0, "active": True,
        }
        # Build payout history
        plist = []
        for _ in range(claims):
            lv = rng.randint(1, 3)
            hours = {1: 2, 2: 3, 3: 4}.get(lv, 3)
            p = calculate_payout(earnings, lv, disruption_hours=hours)
            days_ago = rng.randint(1, days)
            plist.append({
                "date":  (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d"),
                "time":  f"{rng.randint(8,20):02d}:{rng.randint(0,59):02d}",
                "zone":  zone,
                "level": lv,
                "level_label": DISRUPTION_LEVEL_CONFIG[lv]["label"],
                "payout": p,
                "disruption_hours": hours,
                "conditions": {"rain": rng.randint(15, 60), "aqi": rng.randint(100, 350), "temp": rng.randint(28, 42)},
            })
        payouts[phone] = plist
        
        prlist = []
        for w in range(rng.randint(1, 4)):
            prlist.append({
                "txn_id": f"GS{rng.randint(100000,999999)}",
                "amount": premium, "status": "SUCCESS",
                "date": (datetime.now() - timedelta(weeks=w)).strftime("%Y-%m-%d"),
                "time": "09:00", "method": "UPI", "week_of": str(w),
            })
        premium_payments[phone] = prlist

@app.route("/api/admin/stats")
def api_admin_stats():
    """Aggregate stats for insurer console."""
    if not riders:
        _seed_demo_data()

    total_riders   = len(riders)
    active_riders  = sum(1 for r in riders.values() if r.get("active"))
    total_premiums = sum(
        sum(p["amount"] for p in premium_payments.get(ph, []))
        for ph in riders
    )
    total_payouts_amt = sum(
        sum(p["payout"] for p in payouts.get(ph, []))
        for ph in riders
    )
    total_claims = sum(len(payouts.get(ph, [])) for ph in riders)
    loss_ratio = round(total_payouts_amt / total_premiums * 100, 1) if total_premiums else 0

    # Zone breakdown
    zone_stats = {}
    for ph, rider in riders.items():
        z = rider["zone"]
        if z not in zone_stats:
            zone_stats[z] = {"riders": 0, "payouts": 0, "premium_collected": 0}
        zone_stats[z]["riders"] += 1
        zone_stats[z]["payouts"] += sum(p["payout"] for p in payouts.get(ph, []))
        zone_stats[z]["premium_collected"] += sum(p["amount"] for p in premium_payments.get(ph, []))

    # Platform breakdown
    platform_counts = {}
    for r in riders.values():
        p = r["platform"]
        platform_counts[p] = platform_counts.get(p, 0) + 1

    # Trust tier distribution
    tier_dist = {"Bronze": 0, "Silver": 0, "Gold": 0}
    for r in riders.values():
        tier = get_trust_tier(r["trust_score"])["name"]
        tier_dist[tier] += 1

    # Recent payouts (last 10 across all riders)
    all_payouts = []
    for ph, plist in payouts.items():
        rider = riders.get(ph, {})
        for p in plist:
            all_payouts.append({**p, "rider_name": rider.get("name", "—"), "phone": ph})
    all_payouts.sort(key=lambda x: x["date"] + x.get("time", ""), reverse=True)

    return jsonify({
        "summary": {
            "total_riders":       total_riders,
            "active_riders":      active_riders,
            "total_premiums":     round(total_premiums, 2),
            "total_payouts_amt":  round(total_payouts_amt, 2),
            "total_claims":       total_claims,
            "loss_ratio":         loss_ratio,
            "avg_premium":        round(total_premiums / total_riders, 2) if total_riders else 0,
        },
        "zone_stats":       zone_stats,
        "platform_counts":  platform_counts,
        "tier_dist":        tier_dist,
        "recent_payouts":   all_payouts[:10],
        "riders":           [
            {
                "name":           r["name"],
                "zone":           r["zone"],
                "platform":       r["platform"],
                "daily_earnings": r["daily_earnings"],
                "trust_score":    r["trust_score"],
                "tier":           get_trust_tier(r["trust_score"])["name"],
                "premium":        r["premium"],
                "claims":         len(payouts.get(ph, [])),
                "total_paid_out": sum(p["payout"] for p in payouts.get(ph, [])),
                "active":         r.get("active", True),
            }
            for ph, r in riders.items()
        ],
    })


# ─────────────────────────────────────────────────────────────────
# ZONE COMPARISON API
# ─────────────────────────────────────────────────────────────────

@app.route("/api/zone-compare")
def api_zone_compare():
    """Compare all zones: baselines, live conditions, risk score."""
    result = []
    for zone, baseline in ZONE_BASELINES.items():
        conds = simulate_current_conditions(zone)
        risk_score = round(
            (baseline["rain_mm_hr"]["sigma"] / 15 +
             baseline["aqi"]["sigma"] / 50 +
             baseline["temp_c"]["sigma"] / 8) / 3 * 100
        )
        result.append({
            "zone":          zone,
            "city":          baseline["city"],
            "rain_baseline": baseline["rain_mm_hr"]["mu"],
            "aqi_baseline":  baseline["aqi"]["mu"],
            "temp_baseline": baseline["temp_c"]["mu"],
            "current_level": conds["fused_level"],
            "current_label": conds["fused_label"],
            "current_color": conds["fused_color"],
            "risk_score":    risk_score,
            "live_rain":     conds["rain_mm_hr"],
            "live_aqi":      conds["aqi"],
            "live_temp":     conds["temp_c"],
        })
    result.sort(key=lambda x: x["risk_score"], reverse=True)
    return jsonify(result)


# ─────────────────────────────────────────────────────────────────
# PREMIUM CALCULATOR PAGE (public tool)
# ─────────────────────────────────────────────────────────────────

@app.route("/calculator")
def calculator():
    return render_template("calculator.html", zones=ZONES)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

