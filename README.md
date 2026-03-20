# 🛡️ GigShield
### AI-Powered Parametric Income Insurance · India's Delivery Workers

<div align="center">

![Guidewire DEVTrails 2026](https://img.shields.io/badge/Guidewire-DEVTrails%202026-0e6e8c?style=for-the-badge)
![Phase 1 · Seed](https://img.shields.io/badge/Phase-1%20·%20Seed-f5a623?style=for-the-badge)
![Swiggy / Zomato](https://img.shields.io/badge/Persona-Swiggy%20%2F%20Zomato-1a9cbf?style=for-the-badge)
![Income Loss Only](https://img.shields.io/badge/Coverage-Income%20Loss%20Only-27ae60?style=for-the-badge)

> **"We don't insure events — we insure the earning potential lost when events break a rider's ability to work, dynamically personalized to their zone and behaviour."**

</div>

---

## 📎 Quick Links

| Resource                   | Access                                                                                                                                                                    |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 📄 Full Idea Blueprint     | [View Document](https://amritauniv-my.sharepoint.com/:w:/g/personal/am_sc_u4cse23115_am_students_amrita_edu/IQCVzuaYIhchQLL6ajj7_87hAfzg6-X4A--Vp4zjhCjI7nc?e=SzPjhA)     |
| 📊 Pitch Deck (PPT)        | [View Presentation](https://amritauniv-my.sharepoint.com/:p:/g/personal/am_sc_u4cse23115_am_students_amrita_edu/IQC_OlpH3iEfSqNm1FDoLxeiAV4SrmrpWD9JJaTB4TFxFjg?e=rex3kN) |
| 🎥 2-Minute Strategy Video | [Watch Video](https://www.youtube.com/watch?v=pj8aIrwg_rI)                                                                                                                |
| 🗂️ GitHub Repository      | [Open Repository](https://github.com/CholaGanesh05/Guidewire_Devtrails_200-Syndicate) *(main branch)*                                                                     |


## ⚡ The One Idea That Separates Us

Every other team will trigger a static payout when it rains.  
**We ask: how abnormal is this condition for this specific zone, and how much does it truly impact earning potential?**

```
A Bengaluru rider during monsoon    → rain is expected → baseline payout adjusted dynamically
A Jaipur rider during moderate rain → rain is rare     → higher severity payout triggers
A Chennai rider on a 42°C day       → heat is common   → proportional L1/L2 payout based on dynamic local tolerance
A Shimla rider on a 32°C day        → heat is rare     → high L3/L4 payout triggers
```

> **Trigger = dynamic percentage based on deviation from the zone's own historical baseline.**
> It's not a binary "yes/no" — the payout scales proportionally to how severely the local normal is disrupted.

---

## 💡 What GigShield Is

A **dynamically priced parametric income insurance** for Swiggy / Zomato delivery partners, powered by Agentic AI.

- Monitors real-time disruptions across **hyper-local 2–5 km micro-zones**
- **Autonomous Agentic workflows** validate conditions and trigger payouts based on learned local baselines
- Pays via **UPI within 24 hours** — no claim, no call, no paperwork
- Pricing is **dynamically adjusted weekly** per rider zone, season, and trust history

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
AGENTIC AI RISK PROFILING
  Zone baseline built from 90-day historical data
  Seasonal modifier applied (monsoon / heat / cold)
  Rider trust score initialised
        ↓
DYNAMIC WEEKLY PREMIUM → e.g., ₹22 this week (AI-calculated) → Ravi pays via UPI → Policy ACTIVE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WEDNESDAY 3 PM — DISRUPTION DETECTED
  Rain in Koramangala: 48 mm/hr  (zone baseline: 22 mm/hr)  → deviation: +118%
  AQI: 342  (zone safe threshold: 200)                      → deviation: +71%
  Agentic Multi-signal fusion: Rain(L3) + AQI(L2) → Combined = L3

AI VALIDATION (all must pass autonomously)
  Ravi's GPS in disruption zone  ✅
  Swiggy order volume drop −68%  ✅
  No GPS spoof detected          ✅
  No prior claim today           ✅

PAYOUT CALCULATION
  Hourly rate = last 7-day avg earnings ÷ avg active hours = ₹800 ÷ 8 = ₹100/hr
  Estimated lost hours = 4 hrs (peak window blocked)
  Dynamic Payout = 4 × ₹100 × 75% (L3 severity adjusted for local baseline) = ₹300

  → UPI credit processed within 24 hours
  → WhatsApp: "₹300 processing for Koramangala disruption. GigShield has you covered. Stay safe 🛡️"
```

---

## 🧠 The Intelligence Layer

### Agentic AI Orchestrator
Instead of static scripts, autonomous AI agents continuously monitor API streams (weather, traffic, government feeds). When an anomaly is detected, the agent independently cross-references rider GPS and platform demand to validate the disruption and initiate the payout workflow without human intervention.

### Geo-Adaptive Baseline Engine
```
Zone Trigger Threshold = μ(zone, last 90 days) + k × σ(zone)
```
Zone baselines update **weekly**. The system gets smarter — a new construction zone causing traffic anomalies gets learned and priced in within one cycle.

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

### AI Models at a Glance

| Model / Tech | Role |
|---|---|
| Agentic Framework | Autonomous monitoring, multi-step validation, and workflow orchestration |
| XGBoost / LightGBM | Dynamic weekly premium prediction based on multi-factor risk |
| Deep Learning (Regression) | Real-time hourly income estimation |
| Isolation Forest | Unsupervised fraud, spoofing, and anomaly detection |

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

## 💰 Dynamic Weekly Pricing Model

Premiums are not fixed — they are dynamically generated each week using AI to ensure fairness and platform sustainability:

```
Dynamic Base Premium (AI-Generated)
± Zone Risk Score        (historical disruption frequency & severity)
± Seasonal Modifier      (monsoon / summer / winter weighting)
− Trust Discount         (honest + consistent riders pay less)
─────────────────────────────────────────────────────────────
Final Weekly Premium     · Dynamically priced (e.g., ₹15–₹40)
Max Daily Payout         · Capped based on tier (up to ₹600/day)
```

---

## ⚙️ Disruption Levels (Dynamically Weighted)

Payout percentages are proportional to how severely the current condition deviates from the local baseline.

| Level | Condition | Payout |
|---|---|---|
| L0 | Within zone baseline | 0% |
| L1 | Mild deviation | ~25% of estimated lost income |
| L2 | Moderate deviation | ~50% of estimated lost income |
| L3 | High deviation — unsafe / halted work | ~75% of estimated lost income |
| L4 | Complete shutdown / declared disaster | 100% (capped based on tier) |

**Edge cases handled:**
- Rider offline before disruption starts → no payout
- Rider exits disruption zone mid-event → prorated payout
- Disruption lasts < 30 minutes → ignored (noise filter)
- Maximum one payout window per disruption event per rider

---

## 🏗️ Architecture

```
┌───────────────────┬──────────────────────────┬──────────────────────┐
│   DATA INPUTS     │    INTELLIGENCE CORE     │    OUTPUTS           │
├───────────────────┼──────────────────────────┼──────────────────────┤
│ OpenWeatherMap    │ Agentic Orchestrator     │ UPI (Razorpay mock)  │
│ OpenAQ / CPCB     │ Geo Baseline Engine      │ WhatsApp Alerts      │
│ Maps / Traffic    │ Multi-Trigger Fusion     │ Rider Dashboard      │
│ Platform Signal   │ Dynamic Pricing Model    │ Insurer Console      │
│ GPS Feed          │ Isolation Forest (Fraud) │ Predictive Analytics │
│ Gov Alert Feed    │ Trust Score Engine       │ Weekly Audit Log     │
└───────────────────┴──────────────────────────┴──────────────────────┘
        All triggers are zone-relative. Baselines update weekly.
```

---

## 🛠️ Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Rider UX | WhatsApp Business API | Zero install, already used daily |
| AI / Logic | Python + LangChain / LlamaIndex | Agentic AI orchestration and decisioning |
| ML Models | XGBoost · scikit-learn | Dynamic pricing, fraud detection |
| Backend | FastAPI (Python) | High-concurrency real-time processing |
| Database | PostgreSQL + Redis | Persistent data + live zone cache |
| Payments | Razorpay Test Mode | UPI simulation for demo (<24h processing) |
| Geo | Google Maps + Leaflet.js | Zone mapping + GPS validation |
| Weather | OpenWeatherMap (free tier) | Reliable, India-wide coverage |
| AQI | OpenAQ / CPCB (free) | India-specific monitoring nodes |

---

## 🛡️ Fraud Prevention

| Check | Method |
|---|---|
| GPS spoofing | Trajectory velocity anomaly analysis |
| Zone presence | GPS vs disruption boundary cross-check |
| Activity validation | Real order volume drop required to confirm income loss |
| Duplicate accounts | Device fingerprinting + phone deduplication |
| Claim rate abuse | Hard limit — one payout window per disruption per rider |

---

## 🎮 Trust Score

Riders who are honest and consistent earn better terms:

| Tier | Score | Benefit |
|---|---|---|
| 🥉 Bronze | 0–40 | Standard premium and payout cap |
| 🥈 Silver | 41–70 | Discounted premium · +10% payout cap |
| 🥇 Gold | 71–100 | Highest discount · +25% payout cap |

---

## 🌍 Scalability Path

GigShield's engine is persona-agnostic. Phase 1 targets food delivery.  
The same geo-adaptive, agentic model extends to:
**E-commerce (Amazon/Flipkart) → Q-Commerce (Zepto/Blinkit) → Cab drivers (Uber/Ola) → Logistics gig workers**

One engine. Every gig worker in India.

---

## ✅ Phase 1 Checklist

- [x] Unique geo-adaptive positioning defined
- [x] Persona scenario + end-to-end workflow
- [x] Dynamic AI weekly premium model integrated
- [x] L0–L4 proportional trigger system with zone-relative thresholds
- [x] Income estimation model
- [x] Multi-trigger fusion & Agentic AI logic
- [x] AI model breakdown (pricing · fraud · orchestration)
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
| Team Name | 200 Syndicate |
| Team Members | Chola Chetan Chukkala, David Shibu, Evan Binu Chirayath, Jacob Isaac |
| Repository | [CholaGanesh05/Guidewire_Devtrails_200-Syndicate](https://github.com/CholaGanesh05/Guidewire_Devtrails_200-Syndicate) |

---

<div align="center">

*Not just insurance. An autonomous, adaptive income protection engine that understands*
*where you live, how you work, and when the world truly gets in your way.*

**GigShield · Guidewire DEVTrails 2026 · Seed → Scale → Soar 🚀**

</div>
