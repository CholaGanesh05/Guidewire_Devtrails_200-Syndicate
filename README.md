# 🛡️ GigShield — AI-Powered Parametric Income Insurance for Delivery Workers

<div align="center">

![Guidewire DEVTrails 2026](https://img.shields.io/badge/Guidewire-DEVTrails%202026-0e6e8c?style=for-the-badge)
![Phase](https://img.shields.io/badge/Phase-1%20%7C%20Seed-f5a623?style=for-the-badge)
![Persona](https://img.shields.io/badge/Persona-Food%20Delivery%20(Swiggy%2FZomato)-1a9cbf?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-Income%20Loss%20Only-2ecc71?style=for-the-badge)

### *"When the rain stops deliveries, GigShield starts paying."*

*Zero paperwork. Zero waiting. Instant weekly income protection for India's gig workforce.*

</div>

---

## ⚡ The Big Idea — In 30 Seconds

India's **8M+ food delivery partners** earn ₹500–₹1,200/day. One heavy rainstorm, a curfew, or a severe pollution spike wipes out an entire day's wages — and **nobody compensates them**.

**GigShield** is a ₹25/week AI-powered parametric insurance that:

- 🔍 **Monitors** weather, AQI, traffic and social disruptions in real time across hyper-local micro-zones
- ⚡ **Auto-triggers** payouts the moment measurable thresholds are crossed — no claim filing, ever
- 💸 **Pays instantly** via UPI within 60 seconds of trigger validation
- 🧠 **Learns continuously** — dynamic weekly pricing adjusted per rider, zone, behavior and season

> ⚠️ **Strictly income-only coverage.** No health, life, accident, or vehicle repair payouts — ever.

---

## 💡 Novelty — What Makes This Different

| What Exists Today | What GigShield Does |
|---|---|
| Manual claim filing taking days | ✅ Zero-touch parametric auto-trigger |
| Generic city-level weather data | ✅ Hyper-local 2–5 km micro-zone intelligence |
| Flat monthly or annual premiums | ✅ AI-adjusted dynamic **weekly** pricing |
| Single disruption trigger | ✅ Multi-signal fusion (rain + AQI + traffic + platform downtime) |
| App-download-required UX | ✅ WhatsApp-first, multilingual, low-data UX |
| Trust-neutral platforms | ✅ Gamified trust scoring with payout bonuses |
| Insurer-controlled validation | ✅ AI validates using objective, auditable external data |

---

## 👤 Persona — Who We're Building For

**Ravi, 28 | Swiggy Food Delivery Partner | Bengaluru**

> *"Last monsoon I lost 6 days of income. Nobody helped. I had no option but to keep riding in the rain."*

| Attribute | Detail |
|---|---|
| Daily earning | ₹700–₹900 across lunch and dinner peaks |
| Vehicle | Two-wheeler; heavily impacted by rain, heat, AQI |
| Tech comfort | WhatsApp daily user; avoids new app downloads |
| Pain point | Zero safety net for uncontrollable external events |
| Trust need | Transparency in how payouts are calculated |

---

## 🔄 Application Workflow — Persona-Based Scenario

### Scenario: Ravi's First Heavy Monsoon Day Under GigShield

```
WEEK 1 — MONDAY MORNING

  Ravi opens WhatsApp
       ↓
  GigShield Bot: "Namaste Ravi! Protect your week's income for just ₹27."
       ↓
  Ravi enters: Zone (Koramangala) · Platform (Swiggy) · Daily avg (₹800)
       ↓
  [AI Risk Profiler runs]
       Zone flood-risk score: HIGH (monsoon season)
       Historical disruption rate: 2.3 days/month
       Seasonal adjustment: +15% premium modifier
       ↓
  Weekly Premium Generated → ₹27 for this week
       ↓
  Ravi pays via UPI → Policy ACTIVE for Mon–Sun

──────────────────────────────────────────────────────

WEDNESDAY 3:00 PM — DISRUPTION EVENT

  OpenWeatherMap API: Rainfall = 48mm/hr in Koramangala zone
  CPCB AQI API: AQI = 342 (Very Unhealthy)
       ↓
  [GigShield Trigger Engine activates]
       L3 disruption classified: Heavy Rain + Poor AQI
       Confidence score: 94%
       ↓
  [AI Validation Engine cross-checks]
       Ravi's GPS: In active disruption zone ✅
       Swiggy order volume in zone: -68% drop ✅
       No GPS spoofing anomaly detected ✅
       Cooldown check: No prior claim today ✅
       ↓
  [Payout Calculated]
       Lost hours estimated: 4 hrs (peak period blocked)
       Hourly rate: ₹800 ÷ 8 hrs = ₹100/hr
       Payout = 4 hrs × ₹100 × 75% (L3 severity) = ₹300
       ↓
  UPI Transfer → Ravi's account → ₹300 in < 60 seconds
  WhatsApp: "GigShield paid ₹300 for today's rain disruption. Stay safe 🛡️"
```

---

## 📡 Parametric Trigger System

Disruptions are classified across **5 levels (L0–L4)** with automatic payout scaling:

| Level | Trigger Condition | Payout | Example |
|---|---|---|---|
| **L0** | Normal conditions | 0% | Clear skies, normal traffic |
| **L1** | Rain >10mm/hr · AQI 201–300 | 25% | Light monsoon shower |
| **L2** | Rain >35mm/hr · AQI 301–400 | 50% | Heavy rain, reduced visibility |
| **L3** | Flood alert · AQI >400 · Curfew | 75% | Waterlogging, zone shutdown |
| **L4** | Declared disaster · Complete halt | 100% (capped ₹600/day) | Cyclone, state emergency |

**Live Trigger Data Sources:**

| Source | API | Data Used |
|---|---|---|
| Weather | OpenWeatherMap (free tier) | Rainfall mm/hr, wind speed, humidity |
| Air Quality | OpenAQ / CPCB | Real-time AQI readings per zone |
| Traffic | HERE Maps / Google Maps | Congestion index per micro-zone |
| Platform Signal | Simulated mock | Order volume drop percentage |
| Government Alerts | RSS / Gov feed | Curfews, strikes, zone closures |

---

## 💰 Weekly Premium Model

```
┌───────────────────────────────────────────────┐
│         GIGSHIELD PREMIUM CALCULATOR          │
├───────────────────────────────────────────────┤
│  Base Premium              =  ₹20/week        │
│  + Zone Risk Modifier      =  ₹0 to ₹10       │
│    (flood-prone = +₹10 · low-risk = +₹0)      │
│  + Seasonal Modifier       =  ₹0 to ₹5        │
│    (monsoon months = +₹5)                     │
│  − Behavior Discount       =  −₹2 to −₹5      │
│    (high trust score = more savings)          │
├───────────────────────────────────────────────┤
│  Final Weekly Premium      =  ₹15 – ₹35/week  │
│  Maximum Weekly Payout     =  up to ₹600/day  │
└───────────────────────────────────────────────┘
```

- No annual lock-in — renews every Monday
- Cancel anytime; unused days prorated
- Average ₹25/week = roughly 3% of weekly income for most riders

---

## 🧠 AI/ML Integration Plan

### 1. Dynamic Premium Calculation
- **Model:** Gradient Boosted Regressor (XGBoost)
- **Features:** Zone disruption frequency, seasonal risk index, rider consistency score, historical claim rate, AQI baseline per zone
- **Output:** Personalized ₹/week premium recalculated every Monday

### 2. Geo-Adaptive Risk Profiling
- K-means clustering of delivery zones into micro-zones (2–5 km radius)
- Historical weather deviation scoring stored per zone
- Seasonal adjustment matrices for monsoon, summer, winter cycles
- Zone risk score updates weekly from incoming API data

### 3. Fraud Detection Engine

| Check | Method |
|---|---|
| GPS spoofing | Trajectory velocity anomaly detection |
| Zone presence | Cross-validate GPS vs disruption zone boundary |
| Activity validation | Order volume drop from platform signal |
| Behavioral baseline | Inactivity unusual for this rider at this hour? |
| Duplicate accounts | Device fingerprinting + phone deduplication |
| Claim frequency | Rate-limiting per user per disruption event |

### 4. Payout Prediction (Insurer Dashboard)
- Forecasts high-risk disruption days for the coming week
- Pre-positions payout liquidity
- Alerts insurer when >X% of zone riders are likely to claim simultaneously

---

## 🏗️ System Architecture

```
                    ┌──────────────────────────────┐
                    │      GIGSHIELD PLATFORM      │
                    └──────────────────────────────┘

┌───────────────┐   ┌──────────────────────┐   ┌──────────────────┐
│  INPUT LAYER  │   │  INTELLIGENCE LAYER  │   │  OUTPUT LAYER    │
├───────────────┤   ├──────────────────────┤   ├──────────────────┤
│ WhatsApp API  │──▶│ Risk Profiling ML    │──▶│ UPI Payout       │
│ Weather APIs  │   │ Dynamic Pricing      │   │ WhatsApp Alerts  │
│ AQI APIs      │──▶│ Trigger Classifier   │──▶│ Worker Dashboard │
│ Traffic APIs  │   │ Fraud Detection AI   │   │ Insurer Console  │
│ Platform API  │──▶│ Geo-Zone Engine      │──▶│ Audit Logs       │
│ GPS Feed      │   │ Payout Calculator    │   │ Analytics Report │
└───────────────┘   └──────────────────────┘   └──────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Rationale |
|---|---|---|
| Frontend | React.js (Web) | Insurer dashboard + rider portal |
| Bot / UX | WhatsApp Business API | Primary rider interaction — zero install |
| Backend | FastAPI (Python) | High-throughput real-time trigger processing |
| AI / ML | scikit-learn · XGBoost | Pricing + fraud + prediction models |
| Database | PostgreSQL + Redis | Persistent data + real-time zone cache |
| Weather | OpenWeatherMap API | Free tier, reliable, India-wide coverage |
| AQI | OpenAQ / CPCB API | Open-source, India-specific monitoring nodes |
| Payments | Razorpay Test Mode | UPI simulation for Phase 1–2 demo |
| Geo | Google Maps / Leaflet.js | Zone boundary mapping + GPS validation |
| Deployment | Render / Railway | Lightweight Phase 1–2 hosting |

**Platform Choice: Web (React) + WhatsApp Bot**

Riders need zero-friction access via WhatsApp. Insurers need analytics richness via a web dashboard. This dual approach serves both audiences without forcing riders to install anything.

---

## 🎮 Gamification & Trust Score

Every rider builds a **GigShield Trust Score (0–100):**

| Action | Score Impact |
|---|---|
| Consistent active working pattern | +5 / week |
| No fraudulent claim detected | +3 / week |
| Long-term subscriber (4+ weeks) | +2 / week |
| GPS anomaly detected during claim | −20 |
| Duplicate claim attempt | −30 |

**Trust Tier Benefits:**

| Tier | Score Range | Benefit |
|---|---|---|
| 🥉 Bronze | 0–40 | Standard premium · Standard payout cap |
| 🥈 Silver | 41–70 | −₹3/week discount · +10% payout cap |
| 🥇 Gold | 71–100 | −₹5/week discount · +25% payout cap |

---

## 🗺️ Coverage Scope

| ✅ Covered (Income Loss Only) | ❌ Explicitly Excluded |
|---|---|
| Heavy rainfall halting deliveries | Vehicle repairs |
| Extreme heat / dangerous heat index | Medical bills |
| High AQI / severe pollution spike | Accident coverage |
| Flash floods and waterlogging | Health insurance |
| Local curfew / public strike | Life insurance |
| Platform app downtime (simulated) | Property damage |
| Sudden order demand collapse in zone | Personal liability |

---

## 📅 Phase 1 Deliverables Checklist

- [x] Idea document — this README
- [x] Persona-based scenario with workflow
- [x] Weekly premium model fully defined
- [x] Parametric triggers with L0–L4 levels
- [x] AI/ML integration plan detailed
- [x] Fraud detection strategy outlined
- [x] Tech stack and platform choice justified
- [ ] GitHub Repository link *(to be added)*
- [ ] 2-minute strategy video *(to be uploaded)*
- [ ] Detailed 160-point idea document on OneDrive *(to be uploaded)*

---

## 📎 Resources

| Resource | Link |
|---|---|
| 📄 Full Idea Blueprint (160-point detailed document) | *(OneDrive link — to be uploaded)* |
| 🎥 2-Minute Strategy Video | *(YouTube / Drive link — to be uploaded)* |
| 🗂️ GitHub Repository | *(This repository)* |

---

## 👥 Team

| Field | Detail |
|---|---|
| Hackathon | Guidewire DEVTrails 2026 — University Hackathon |
| Partner | EY (Ernst and Young) |
| Phase | 1 — Seed: Ideation and Foundation |
| Submission Deadline | March 20, 2026 |
| Participant | Chola Chetan Chukkala |

---

<div align="center">

*Built for the 8 million delivery partners who power India's digital economy*
*— and deserve a safety net when the world gets in their way.*

**GigShield** · Guidewire DEVTrails 2026 · Seed → Scale → Soar 🚀

</div>
