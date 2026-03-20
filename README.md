# 🛡️ GigShield
### AI-Powered Parametric Income Insurance · India's Delivery Workers

<div align="center">

![Guidewire DEVTrails 2026](https://img.shields.io/badge/Guidewire-DEVTrails%202026-0e6e8c?style=for-the-badge)
![Phase 1 · Seed](https://img.shields.io/badge/Phase-1%20·%20Seed-f5a623?style=for-the-badge)
![Swiggy / Zomato](https://img.shields.io/badge/Persona-Swiggy%20%2F%20Zomato-1a9cbf?style=for-the-badge)
![Income Loss Only](https://img.shields.io/badge/Coverage-Income%20Loss%20Only-27ae60?style=for-the-badge)

> **"We don't insure events — we insure the earning potential lost when events break a rider's ability to work, personalized to their zone and behaviour."**

</div>

---

## 📎 Quick Links

| | |
|---|---|
| 📘 [Guidewire DEVTrails Problem Booklet](#) | *(link)* |
| 📄 [Full Idea Blueprint — 160-point Detail Doc](#) | *(OneDrive — to be added)* |
| 🎥 [2-Minute Strategy Video](#) | *(YouTube / Drive — to be added)* |
| 🗂️ [GitHub Repository](https://github.com/CholaGanesh05/Guidewire_Devtrails_200-Syndicate) | `main` branch |

---

## ⚡ The One Idea That Separates Us

Every other team will trigger a payout when it rains.  
**We ask: is this rain abnormal for this specific zone?**

```
A Bengaluru rider during monsoon   →  rain is NORMAL   →  no payout
A Jaipur rider during moderate rain →  rain is RARE     →  payout triggers
A Chennai rider on a 42°C day      →  heat is NORMAL   →  no payout
A Shimla rider on a 32°C day       →  heat is RARE     →  payout triggers
```

> **Trigger = deviation beyond the zone's own historical baseline, not a fixed global number.**  
> This is what makes GigShield fair — and unfakeable.

---

## 💡 What GigShield Is

A **₹25/week parametric income insurance** for Swiggy / Zomato delivery partners.

- Monitors real-time disruptions across **hyper-local 2–5 km micro-zones**
- **Auto-triggers payouts** only when conditions break the zone's learned normal
- Pays via **UPI in under 60 seconds** — no claim, no call, no paperwork
- Pricing is **AI-adjusted weekly** per rider zone, season, and trust history

> ⚠️ Income loss **only**. No health, accidents, vehicle, or life coverage. Ever.

---

## 👤 Who We're Building For

**Ravi, 28 | Swiggy Partner | Bengaluru**
Lost 6 days of income last monsoon. Zero compensation. Had no choice but to ride in dangerous conditions because stopping meant no money. Uses WhatsApp daily, will not install a new app, earns ₹800/day and lives week to week.

---

## 🔄 End-to-End Flow

```
ONBOARD (2 min via WhatsApp)
  Name · Zone · Platform · Avg daily earnings
        ↓
AI RISK PROFILE
  Zone baseline built from 90-day historical data
  Seasonal modifier applied (monsoon / heat / cold)
  Rider trust score initialised
        ↓
WEEKLY PREMIUM GENERATED  →  ₹27 this week  →  Ravi pays via UPI  →  Policy ACTIVE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WEDNESDAY 3 PM — DISRUPTION DETECTED
  Rain in Koramangala: 48 mm/hr  (zone baseline: 22 mm/hr)  → deviation: +118%
  AQI: 342  (zone safe threshold: 200)                       → deviation: +71%
  Multi-signal fusion: Rain(L3) + AQI(L2) → Combined = L3

VALIDATE (all must pass)
  Ravi's GPS in disruption zone  ✅
  Swiggy order volume drop −68%  ✅
  No GPS spoof detected          ✅
  No prior claim today           ✅

PAYOUT
  Hourly rate = last 7-day avg earnings ÷ avg active hours = ₹800 ÷ 8 = ₹100/hr
  Estimated lost hours = 4 hrs (peak window blocked)
  Payout = 4 × ₹100 × 75% (L3 severity) = ₹300

  → UPI credit in < 60 seconds
  → WhatsApp: "₹300 credited. GigShield covered your disruption. Stay safe 🛡️"
```

---

## 🧠 The Intelligence Layer

### Geo-Adaptive Baseline Engine
```
Zone Trigger Threshold = μ(zone, last 90 days) + k × σ(zone)
```
Zone baselines update **weekly**. The system gets smarter — a new construction zone
causing traffic anomalies gets learned and priced in within one cycle.

### Income Estimation Model
Payout is never a flat number. It reflects actual earning potential:
```
Hourly Rate = f( last 7-day earnings, peak-hour multiplier, zone demand density )
```
New riders without history default to city-wide median until 2 weeks of data is built.

### Multi-Trigger Fusion
Single disruptions rarely capture full impact. GigShield combines signals:
```
Rain(L2) + Traffic(L2) + Demand Drop(L3)  →  fused score  →  L3 payout
```
Prevents underestimation of real-world compound disruptions.

### AI Models at a Glance
| Model | Role |
|---|---|
| XGBoost | Dynamic weekly premium prediction |
| Regression | Real-time hourly income estimation |
| Isolation Forest | Fraud and anomaly detection |
| Time-series (ARIMA) | Disruption forecasting for insurer dashboard |

---

## 📡 What We Cover — Beyond Weather

| Disruption | How Detected |
|---|---|
| Rain / flood beyond zone baseline | OpenWeatherMap API |
| Heat index beyond zone tolerance | Weather + humidity fusion |
| AQI spike above zone safe threshold | CPCB / OpenAQ API |
| Platform app downtime | Platform signal mock |
| Sudden order volume collapse | Demand anomaly model |
| Curfew / strike / zone closure | Government RSS alert feed |
| Traffic lockdown blocking zone | Maps API congestion index |

---

## 💰 Weekly Pricing Model

```
Base Premium              ₹20 / week
+ Zone Risk Score         ₹0–10   (historical disruption frequency)
+ Seasonal Modifier       ₹0–5    (monsoon +5 · summer +3 · winter +0)
− Trust Discount          ₹0–5    (honest + consistent riders pay less)
────────────────────────────────────
Weekly Premium            ₹15–35  · No lock-in · Renews every Monday
Max Daily Payout          ₹600    · Capped regardless of disruption level
```

---

## ⚙️ Disruption Levels

| Level | Condition | Payout |
|---|---|---|
| L0 | Within zone baseline | 0% |
| L1 | Mild deviation | 25% of estimated lost income |
| L2 | Moderate deviation | 50% |
| L3 | High deviation — unsafe / halted | 75% |
| L4 | Complete shutdown / declared disaster | 100% (capped ₹600/day) |

**Edge cases handled:**
- Rider offline before disruption starts → no payout
- Rider exits disruption zone mid-event → prorated payout
- Disruption lasts < 30 minutes → ignored (noise filter)
- Maximum one payout window per disruption event per rider

---

## 🏗️ Architecture

```
┌───────────────────┬──────────────────────────┬──────────────────────┐
│   DATA INPUTS     │    INTELLIGENCE CORE      │   OUTPUTS            │
├───────────────────┼──────────────────────────┼──────────────────────┤
│ OpenWeatherMap    │ Geo Baseline Engine       │ UPI (Razorpay mock)  │
│ OpenAQ / CPCB     │ Multi-Trigger Fusion      │ WhatsApp Alerts      │
│ Maps / Traffic    │ XGBoost Premium ML        │ Rider Dashboard      │
│ Platform Signal   │ Income Estimation Model   │ Insurer Console      │
│ GPS Feed          │ Isolation Forest (Fraud)  │ Predictive Analytics │
│ Gov Alert Feed    │ Trust Score Engine        │ Weekly Audit Log     │
└───────────────────┴──────────────────────────┴──────────────────────┘
        All triggers are zone-relative. Baselines update weekly.
```

---

## 🛠️ Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Rider UX | WhatsApp Business API | Zero install, already used daily |
| Dashboard | React.js | Insurer analytics + rider portal |
| Backend | FastAPI (Python) | Real-time trigger processing |
| AI / ML | XGBoost · scikit-learn | Pricing, fraud, forecasting |
| Database | PostgreSQL + Redis | Persistent data + live zone cache |
| Payments | Razorpay Test Mode | UPI simulation for demo |
| Geo | Google Maps + Leaflet.js | Zone mapping + GPS validation |
| Weather | OpenWeatherMap (free) | Reliable, India-wide |
| AQI | OpenAQ / CPCB (free) | India-specific monitoring nodes |

---

## 🛡️ Fraud Prevention

| Check | Method |
|---|---|
| GPS spoofing | Trajectory velocity anomaly analysis |
| Zone presence | GPS vs disruption boundary cross-check |
| Activity validation | Real order volume drop required to confirm income loss |
| Duplicate accounts | Device fingerprinting + phone deduplication |
| Claim rate abuse | Hard limit: one payout window per disruption per rider |

---

## 🎮 Trust Score

Riders who are honest and consistent earn better terms:

| Tier | Score | Benefit |
|---|---|---|
| 🥉 Bronze | 0–40 | Standard premium and payout cap |
| 🥈 Silver | 41–70 | −₹3/week · +10% payout cap |
| 🥇 Gold | 71–100 | −₹5/week · +25% payout cap |

---

## 🌍 Scalability Path

GigShield's engine is persona-agnostic. Phase 1 targets food delivery.  
The same geo-adaptive model extends to:
**E-commerce (Amazon/Flipkart) → Q-Commerce (Zepto/Blinkit) → Cab drivers (Uber/Ola) → Logistics gig workers**

One engine. Every gig worker in India.

---

## ✅ Phase 1 Checklist

- [x] Unique geo-adaptive positioning defined
- [x] Persona scenario + end-to-end workflow
- [x] Weekly dynamic premium model
- [x] L0–L4 trigger system with zone-relative thresholds
- [x] Income estimation model
- [x] Multi-trigger fusion logic
- [x] AI model breakdown (pricing · fraud · forecasting)
- [x] Edge case handling
- [x] Fraud detection strategy
- [x] Tech stack + platform justified
- [x] Scalability path outlined
- [x] [GitHub Repository](https://github.com/CholaGanesh05/Guidewire_Devtrails_200-Syndicate)
- [ ] 2-minute strategy video — to be uploaded
- [ ] Detailed idea doc on OneDrive — to be uploaded

---

## 👥 Team

| | |
|---|---|
| Hackathon | Guidewire DEVTrails 2026 · University Hackathon · In partnership with EY |
| Phase | 1 — Seed: Ideation & Foundation · Deadline: March 20, 2026 |
| Participant | Chola Chetan Chukkala |
| Repository | [CholaGanesh05/Guidewire_Devtrails_200-Syndicate](https://github.com/CholaGanesh05/Guidewire_Devtrails_200-Syndicate) |

---

<div align="center">

*Not just insurance. An adaptive income protection engine that understands*  
*where you live, how you work, and when the world truly gets in your way.*

**GigShield · Guidewire DEVTrails 2026 · Seed → Scale → Soar 🚀**

</div>
