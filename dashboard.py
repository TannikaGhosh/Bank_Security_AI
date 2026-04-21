# dashboard.py
# Complete AI-Powered Cybersecurity Threat Detection (Banking Fraud + Network Intrusion)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import os
import joblib

# ----------------------------- PAGE CONFIG ---------------------------------
st.set_page_config(
    page_title="AI Cyber Threat Detection", page_icon="🛡️", layout="wide"
)

# ----------------------------- BANK CONTACT --------------------------------
BANK_EMAIL = "mstannikaghosh.2026@gmail.com"

# ----------------------------- USER DATABASE -------------------------------
USERS = {
    "Rameshwar Dasgupta": {
        "password": "R@D@1995",
        "question": "What is your favourite food?",
        "answer": "Dosa",
        "limit": 50000,
        "email": "rameshwar.dasgupta@example.com",
    },
    "Tapan Kumar Jaswal": {
        "password": "123T@pan",
        "question": "What is your hobby?",
        "answer": "painting abstract",
        "limit": 70000,
        "email": "tapan.jaswal@example.com",
    },
    "Tapati Shanal": {
        "password": "T@pati35",
        "question": "What is your born place?",
        "answer": "Maniktala, Mumbai",
        "limit": 35000,
        "email": "tapati.shanal@example.com",
    },
    "Ravi Sethi": {
        "password": "90R@vi",
        "question": "What is your favourite food?",
        "answer": "chowmin with curd",
        "limit": 90000,
        "email": "ravi.sethi@example.com",
    },
    "Tina Samuel": {
        "password": "20Tin@@",
        "question": "What is your hobby?",
        "answer": "painting",
        "limit": 20000,
        "email": "tina.samuel@example.com",
    },
    "Dona Ghosh": {
        "password": "65doN@",
        "question": "What is your sibling name?",
        "answer": "Tina Samuel",
        "limit": 65000,
        "email": "dona.ghosh@example.com",
    },
}

# ----------------------------- LOAD NETWORK MODEL (if exists) --------------
try:
    net_model = joblib.load("cybersecurity_model.pkl")
    scaler = joblib.load("scaler.pkl")
    network_model_available = True
except Exception:
    network_model_available = False
    st.sidebar.warning(
        "Network intrusion model not found. Run src/train_model.py first."
    )


# ----------------------------- THREAT SCORE FUNCTION -----------------------
def compute_threat_score(password_ok, answer_ok, amount_ok, network_features=None):
    score = 0.0
    if not password_ok:
        score += 0.6
    if not answer_ok:
        score += 0.5
    if not amount_ok:
        score += 0.6  # FIXED: higher penalty for exceeding limit
    # If network model is available, add its anomaly score (simulated)
    if network_model_available and network_features is not None:
        # In a real system, you'd call model.predict_proba()
        # Here we simulate a small adjustment
        net_score = np.random.uniform(0, 0.2)  # dummy
        score = min(score + net_score, 1.0)
    return min(score, 1.0)


def make_decision(score):
    if score > 0.8:
        return "BLOCKED", "HIGH RISK - Transaction blocked"
    elif score >= 0.5:
        return "FLAGGED", "MEDIUM RISK - Human analyst review"
    else:
        return "ALLOWED", "LOW RISK - Transaction approved"


# ----------------------------- SAVE LOG ------------------------------------
def save_transaction(
    user_name, password_ok, answer_ok, amount, amount_ok, score, decision, message
):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_name,
        "password_ok": password_ok,
        "answer_ok": answer_ok,
        "amount_requested": amount,
        "user_limit": USERS[user_name]["limit"],
        "amount_within_limit": amount_ok,
        "threat_score": round(score, 2),
        "decision": decision,
        "alert_message": message,
    }
    new_entry = pd.DataFrame([log_entry])
    if os.path.exists("bank_logs.csv"):
        existing = pd.read_csv("bank_logs.csv")
        updated = pd.concat([existing, new_entry], ignore_index=True)
    else:
        updated = new_entry
    updated.to_csv("bank_logs.csv", index=False)
    return updated


# ----------------------------- LOAD LOGS -----------------------------------
@st.cache_data(ttl=5)
def load_logs():
    if os.path.exists("bank_logs.csv"):
        df = pd.read_csv("bank_logs.csv")
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    return pd.DataFrame()


# ----------------------------- SESSION STATE FOR ATTEMPT LIMIT ------------
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "blocked_until" not in st.session_state:
    st.session_state.blocked_until = None

# ----------------------------- DASHBOARD UI --------------------------------
st.title("🛡️ AI-Powered Cybersecurity Threat Detection")
st.markdown(f"**Bank Security Contact:** `{BANK_EMAIL}`")
st.markdown("---")

left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("🔐 Simulate a Transaction (Threat Detection)")

    # Check temporary lockout
    if (
        st.session_state.blocked_until
        and datetime.now() < st.session_state.blocked_until
    ):
        st.error(
            f"❌ Too many failed attempts. Locked until {st.session_state.blocked_until.strftime('%H:%M:%S')}"
        )
        transaction_disabled = True
    else:
        transaction_disabled = False
        if (
            st.session_state.blocked_until
            and datetime.now() >= st.session_state.blocked_until
        ):
            st.session_state.attempts = 0
            st.session_state.blocked_until = None

    with st.form("transaction_form"):
        user_name = st.selectbox("Select Customer", list(USERS.keys()))
        password = st.text_input("Password", type="password")
        question = USERS[user_name]["question"]
        answer = st.text_input(f"Personal Question: {question}")
        amount = st.number_input("Withdrawal Amount (INR)", min_value=0.0, step=1000.0)
        submit = st.form_submit_button(
            "Submit Transaction", disabled=transaction_disabled
        )

    if submit and not transaction_disabled:
        password_ok = password == USERS[user_name]["password"]
        answer_ok = answer.strip().lower() == USERS[user_name]["answer"].lower()
        amount_ok = amount <= USERS[user_name]["limit"]

        # Optionally get network features (simulated)
        net_features = None
        if network_model_available:
            net_features = np.random.rand(41)  # dummy

        score = compute_threat_score(password_ok, answer_ok, amount_ok, net_features)
        decision, message = make_decision(score)

        save_transaction(
            user_name,
            password_ok,
            answer_ok,
            amount,
            amount_ok,
            score,
            decision,
            message,
        )

        # Show result with email and timestamp
        if decision == "ALLOWED":
            st.success(
                f"✅ **{decision}**\n\n{message}\n\n📧 Customer email: {USERS[user_name]['email']}\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            st.session_state.attempts = 0
        elif decision == "FLAGGED":
            st.warning(
                f"⚠️ **{decision}**\n\n{message}\n\n📧 Customer email: {USERS[user_name]['email']}\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n👤 Flagged for manual review."
            )
            st.session_state.attempts = 0
        else:  # BLOCKED
            st.error(
                f"🚨 **{decision}**\n\n{message}\n\n📧 Customer email: {USERS[user_name]['email']}\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n🔒 Access denied. Alert sent."
            )
            st.session_state.attempts += 1
            if st.session_state.attempts >= 2:
                st.session_state.blocked_until = datetime.now().replace(
                    second=0, microsecond=0
                ) + pd.Timedelta(minutes=5)
                st.error("🚫 2 failed attempts. Dashboard locked for 5 minutes.")

        st.cache_data.clear()

with right_col:
    st.subheader("📊 Live Threat Metrics")
    df = load_logs()
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Transactions", len(df))
        col2.metric("Blocked", len(df[df["decision"] == "BLOCKED"]))
        col3.metric("Flagged", len(df[df["decision"] == "FLAGGED"]))
    else:
        st.info("No transactions yet. Submit one above.")

# ----------------------------- FULL WIDTH CHARTS ---------------------------
st.markdown("---")
st.subheader("📈 Threat Analytics Dashboard")

if not df.empty:
    # Pie chart of decisions
    decision_counts = df["decision"].value_counts().reset_index()
    decision_counts.columns = ["Decision", "Count"]
    fig_pie = px.pie(
        decision_counts,
        values="Count",
        names="Decision",
        color="Decision",
        color_discrete_map={"ALLOWED": "green", "FLAGGED": "orange", "BLOCKED": "red"},
        title="Risk Decision Distribution",
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Threat score trend over time
    if len(df) > 1:
        df_sorted = df.sort_values("timestamp")
        fig_line = px.line(
            df_sorted,
            x="timestamp",
            y="threat_score",
            color="decision",
            markers=True,
            title="Threat Score Over Time",
            labels={"threat_score": "Threat Score (0-1)", "timestamp": "Time"},
        )
        fig_line.add_hline(
            y=0.8, line_dash="dash", line_color="red", annotation_text="Block (0.8)"
        )
        fig_line.add_hline(
            y=0.5, line_dash="dash", line_color="orange", annotation_text="Flag (0.5)"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Need at least 2 transactions for trend line.")

    # Recent high-risk alerts (score > 0.5)
    st.subheader("🚨 Recent High-Risk Alerts")
    high_risk = df[df["threat_score"] > 0.5].sort_values("timestamp", ascending=False)
    if not high_risk.empty:
        st.dataframe(
            high_risk[
                [
                    "timestamp",
                    "user",
                    "amount_requested",
                    "threat_score",
                    "decision",
                    "alert_message",
                ]
            ],
            use_container_width=True,
        )
    else:
        st.success("No high-risk alerts. System is secure.")
else:
    st.info("No data yet. Submit a transaction to see charts.")

# Download logs button
if not df.empty:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Full Logs (CSV)",
        data=csv,
        file_name="bank_logs.csv",
        mime="text/csv",
    )

st.markdown("---")
st.markdown(f"🔒 **Report suspicious activity to:** `{BANK_EMAIL}`")
st.markdown("🛡️ AI-powered threat detection | 2‑attempt lockout | Real‑time monitoring")
