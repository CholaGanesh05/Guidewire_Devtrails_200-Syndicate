# 🛡️ GigShield
### AI-Powered Parametric Income Insurance for India's Delivery Workers

<div align="center">

![Guidewire DEVTrails 2026](https://img.shields.io/badge/Guidewire-DEVTrails%202026-0e6e8c?style=for-the-badge)
![Phase 1](https://img.shields.io/badge/Phase-1%20·%20Seed-f5a623?style=for-the-badge)
![Persona](https://img.shields.io/badge/Persona-Swiggy%20%2F%20Zomato-1a9cbf?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-Income%20Loss%20Only-27ae60?style=for-the-badge)

**"It's not about rain. It's about rain *beyond what your zone can handle.*"**

</div>

---

## 📎 Resources

| | Link |
|---|---|
| 📘 Guidewire DEVTrails Problem Booklet | *(link)* |
| 📄 Full Idea Blueprint (detailed document) | *(OneDrive link — to be added)* |
| 🎥 2-Minute Strategy Video | *(YouTube / Drive — to be added)* |

---

## ⚡ The Core Insight — What Sets Us Apart

Every other team will build a weather insurance product.  
**We're building a local-intelligence disruption engine.**

> A Bengaluru rider **is not paid** just because it rained during monsoon — that's normal for them.  
> A Jaipur rider **is paid** when it rains moderately — because that's rare, disruptive, and genuinely impacts their income.

**GigShield's trigger = deviation from YOUR zone's historical baseline**, not a fixed global threshold.  
That's the difference between a generic product and one that's actually fair.

---

## 💡 What Is GigShield?

A **₹25/week parametric income insurance** for Swiggy / Zomato delivery partners that:

- Monitors disruptions in real time across **hyper-local 2–5 km micro-zones**
- **Auto-triggers payouts** when conditions deviate beyond the zone's tolerance — no claims, ever
- Pays via **UPI in under 60 seconds**
- Adjusts weekly pricing dynamically using **AI risk profiling per rider + zone**

> ⚠️ Income loss only. Zero coverage for health, accidents, vehicles, or life.

---

## 🧠 The Geo-Adaptive Logic (Our Key Differentiator)

```
Trigger Threshold = Historical Zone Average  +  (k × Zone Std. Deviation)

Kerala  → Heavy rain is normal → Threshold is HIGH → Only extreme flooding triggers
Jaipur  → Rain is rare        → Threshold is LOW  → Even moderate rain triggers
Chennai → Heat is normal      → Threshold is HIGH → Only dangerous heat index triggers
Shimla  → Cold is normal      → Threshold is LOW  → Platform outage triggers faster
```

**The AI learns each zone's "normal" — and triggers only when reality breaks it.**  
This means fair premiums, honest payouts, and zero over-claiming.

---

## 👤 Persona

**Ravi, 28 | Swiggy Partner | Bengaluru | Earns ₹800/day**

- Lost 6 days of income last monsoon with zero compensation
- Rides a two-wheeler; affected by rain, heat, AQI spikes
- WhatsApp user daily; will not download a new app
- Needs a system that's transparent, instant, and requires zero effort

---

## 🔄 How It Works — Ravi's Story

```
Monday      → WhatsApp onboarding (2 mins) → AI profiles Ravi's zone → ₹27/week generated → UPI pay → Policy active

Wednesday   → Rainfall in Koramangala zone spikes beyond historical baseline
            → AQI crosses zone tolerance level
            → GigShield classifies: L3 Disruption

AI Validates → Ravi's GPS is in zone ✅  |  Order volume dropped 68% ✅  |  No GPS spoof ✅

Payout      → 4 lost hrs × ₹100/hr × 75% severity = ₹300 via UPI < 60 seconds
            → WhatsApp: "₹300 credited. Stay safe today 🛡️"
```

---

## 📡 What We Cover — Beyond Just Weather

Most teams stop at weather. We cover every measurable disruption that kills income:

| Disruption | Trigger Source |
|---|---|
| Rain / flood exceeding zone baseline | Weather API |
| Heat index beyond zone tolerance | Weather + humidity API |
| AQI spike above zone's safe threshold | CPCB / OpenAQ API |
| Platform app downtime (Swiggy/Zomato) | Platform signal (mock) |
| Sudden order volume collapse in zone | Demand anomaly detection |
| Curfew / local strike / zone closure | Government alert feed |
| Traffic lockdown blocking zone access | Maps API congestion index |

---

## 💰 Weekly Premium — How Pricing Works

```
Base Premium           ₹20 / week  (all riders)
+ Zone Risk Score      ₹0–₹10      (based on historical disruption frequency)
+ Seasonal Modifier    ₹0–₹5       (monsoon / summer / winter adjustment)
− Trust Discount       ₹0–₹5       (consistent, honest riders pay less)
─────────────────────────────────────────────
Final Weekly Premium   ₹15–₹35     No annual lock-in. Renews every Monday.
Max Daily Payout       ₹600        Capped regardless of disruption level.
```

---

## ⚙️ Disruption Levels & Payouts

| Level | What It Means | Payout |
|---|---|---|
| L0 | Normal — within zone baseline | 0% |
| L1 | Mild deviation — minor income impact | 25% |
| L2 | Moderate deviation — clear income loss | 50% |
| L3 | High deviation — unsafe / halted work | 75% |
| L4 | Shutdown — declared or complete halt | 100% (capped ₹600/day) |

---

## 🏗️ Architecture (High Level)

```
┌─────────────────────────────────────────────────────────────────┐
│                        GIGSHIELD ENGINE                         │
├──────────────────┬──────────────────────┬───────────────────────┤
│   DATA INPUTS    │   INTELLIGENCE CORE  │   OUTPUTS             │
├──────────────────┼──────────────────────┼───────────────────────┤
│ OpenWeatherMap   │ Geo Baseline Engine  │ UPI Payout (Razorpay) │
│ OpenAQ / CPCB    │ Disruption Classifier│ WhatsApp Alerts       │
│ Maps / Traffic   │ XGBoost Pricing ML   │ Rider Dashboard       │
│ Platform Signal  │ Fraud Detection AI   │ Insurer Console       │
│ GPS Feed         │ Payout Calculator    │ Weekly Analytics      │
│ Gov Alert Feed   │ Trust Score Engine   │ Audit Log             │
└──────────────────┴──────────────────────┴───────────────────────┘
         ↑ All triggers are zone-relative, not globally fixed ↑
```

---

## 🛠️ Tech Stack

| Layer | Choice |
|---|---|
| Rider UX | WhatsApp Business API (zero install) |
| Insurer Dashboard | React.js |
| Backend | FastAPI (Python) |
| AI / ML | XGBoost + scikit-learn |
| Database | PostgreSQL + Redis |
| Payments | Razorpay Test Mode (UPI mock) |
| Geo / Maps | Google Maps API + Leaflet.js |
| Weather | OpenWeatherMap (free tier) |
| AQI | OpenAQ / CPCB (free) |

**Why Web + WhatsApp?** Riders need zero friction (WhatsApp). Insurers need analytics depth (Web). No rider has to install anything.

---

## 🛡️ Fraud Detection — Key Checks

- GPS location during claim vs actual disruption zone boundary
- Rider activity signal vs claimed inactivity
- Trajectory analysis to detect GPS spoofing
- Order volume in zone to validate demand collapse claims
- Device fingerprinting + phone deduplication (no multi-accounts)
- Claim frequency rate-limiting per disruption window

---

## 🎮 Trust Score — Riders Who Play Fair, Win More

Honest, consistent riders build a **Trust Score (0–100)** that reduces premiums and raises payout caps:

| Tier | Score | Benefit |
|---|---|---|
| 🥉 Bronze | 0–40 | Standard terms |
| 🥈 Silver | 41–70 | −₹3/week · +10% payout cap |
| 🥇 Gold | 71–100 | −₹5/week · +25% payout cap |

---

## ✅ Phase 1 Checklist

- [x] Core idea + unique geo-adaptive positioning defined
- [x] Persona-based scenario with live workflow
- [x] Weekly premium model with dynamic pricing logic
- [x] Parametric trigger system (L0–L4) with zone-relative thresholds
- [x] AI/ML plan — pricing, fraud detection, prediction
- [x] Full coverage scope beyond weather
- [x] Tech stack + platform justified
- [] GitHub repository link *https://github.com/CholaGanesh05/Guidewire_Devtrails_200-Syndicate*
- [ ] 2-minute strategy video *(upload before submission)*
- [ ] Detailed idea document on OneDrive *(upload before submission)*

---

## 👥 Team

| | |
|---|---|
| Hackathon | Guidewire DEVTrails 2026 · University Hackathon |
| Partner | EY (Ernst & Young) |
| Phase | 1 — Seed: Ideation & Foundation |
| Deadline | March 20, 2026 |
| Participant | Chola Chetan Chukkala |

---

<div align="center">

*Not just insurance. An income protection engine that actually understands where you live and how you work.*

**GigShield · Seed → Scale → Soar 🚀**

</div>
