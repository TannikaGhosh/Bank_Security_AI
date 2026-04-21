# 🛡️ AI-Powered Cybersecurity Threat Detection (Bank_Security_AI)

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red.svg)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-orange.svg)](https://scikit-learn.org/)

## 📌 Project Overview
This system detects cyber threats in real‑time by combining **network intrusion detection** (NSL‑KDD dataset) with **banking fraud detection** (user authentication, withdrawal limits). It assigns a **threat score** and decides to **ALLOW**, **FLAG** (human review), or **BLOCK** transactions. Includes a live Streamlit dashboard, 2‑attempt lockout, and simulated email alerts.

## 🎯 Problem Statement
Traditional security rules fail against zero‑day attacks. AI analyses patterns (login failures, abnormal amounts) to catch fraud and intrusions. This project simulates a bank’s security operations centre (SOC).

## 🏗️ Architecture
- **Data**: NSL‑KDD (network traffic) + 6 synthetic user profiles.
- **Model**: Random Forest (binary classification: normal vs attack).
- **Threat scoring**: Weighted sum of failed password, wrong answer, amount over limit.
- **Decision thresholds**: >0.8 → BLOCK; 0.5–0.8 → FLAG; <0.5 → ALLOW.
- **Dashboard**: Streamlit with pie chart, trend line, alerts table, CSV logs.

## 🛠️ Tech Stack
- Python 3.12, Pandas, Scikit‑learn, Joblib
- Streamlit, Plotly, Matplotlib
- NSL‑KDD dataset

## 📊 Results
- Random Forest accuracy on NSL‑KDD: **~99%**
- Threat scoring correctly blocks >90% of fraudulent attempts (tested with 6 users)
- Dashboard shows real‑time risk distribution

## 🚀 Installation & Run

```bash
# Clone repository
git clone https://github.com/yourusername/Bank_Security_AI.git
cd Bank_Security_AI

# Create virtual environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Train the network intrusion model (one time)
python src/train_model.py

# Launch dashboard
streamlit run dashboard.py
```

## 📸 Screenshots

| Dashboard main | Threat alert |
|----------------|---------------|
| ![Dashboard](images/dashboard_main.png) | ![Alert](images/threat_alert.png) |

| Pie chart | Trend line |
|-----------|-------------|
| ![Pie](images/pie_chart.png) | ![Trend](images/trend_line.png) |

## 📈 Learning Outcomes
- Applied ML to cybersecurity (intrusion detection + fraud prevention)
- Built interactive dashboard with Streamlit
- Implemented session‑based rate limiting (2‑attempt lockout)
- Simulated real‑time alerting and logging

## 🔮 Future Improvements
- Deploy as cloud API (AWS Lambda)
- Integrate real SMTP email alerts
- Add live packet capture with Scapy

## 📧 Contact
Bank Security Email: `mstannikaghosh.2026@gmail.com`

---
*This project was built as a proof of work for placements and internships.*
