# bank_system.py
# AI-Powered Banking Security System with Threat Score & Email Alerts (Simulated)

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import sys

# ======================== 1. USER DATABASE (with fake emails) ========================
users = {
    "Rameshwar Dasgupta": {
        "password": "R@D@1995",
        "question": "What is your favourite food?",
        "answer": "Dosa",
        "limit": 50000,
        "email": "rameshwar.dasgupta@example.com"
    },
    "Tapan Kumar Jaswal": {
        "password": "123T@pan",
        "question": "What is your hobby?",
        "answer": "painting abstract",
        "limit": 70000,
        "email": "tapan.jaswal@example.com"
    },
    "Tapati Shanal": {
        "password": "T@pati35",
        "question": "What is your born place?",
        "answer": "Maniktala, Mumbai",
        "limit": 35000,
        "email": "tapati.shanal@example.com"
    },
    "Ravi Sethi": {
        "password": "90R@vi",
        "question": "What is your favourite food?",
        "answer": "chowmin with curd",
        "limit": 90000,
        "email": "ravi.sethi@example.com"
    },
    "Tina Samuel": {
        "password": "20Tin@@",
        "question": "What is your hobby?",
        "answer": "painting",
        "limit": 20000,
        "email": "tina.samuel@example.com"
    },
    "Dona Ghosh": {
        "password": "65doN@",
        "question": "What is your sibling name?",
        "answer": "Tina Samuel",
        "limit": 65000,
        "email": "dona.ghosh@example.com"
    }
}

# Bank email (your provided email)
BANK_EMAIL = "mstannikaghosh.2026@gmail.com"

# ======================== 2. SIMULATED EMAIL ALERT ========================
def send_alert_simulation(customer_name, customer_email, amount, score, decision, message):
    """Simulates sending an email  prints details instead of actually sending"""
    print("\n" + "="*60)
    print(f" [SIMULATED EMAIL]")
    print(f"   From (Bank): {BANK_EMAIL}")
    print(f"   To: {customer_email} (Customer: {customer_name})")
    print(f"   Subject:  Security Alert - Transaction {decision}")
    print(f"   Message:")
    print(f"   Dear {customer_name},")
    print(f"   Your transaction of INR {amount} has been {decision}.")
    print(f"   Threat Score: {score}")
    print(f"   Reason: {message}")
    print(f"   If this was not you, please contact bank immediately.")
    print("="*60)

# ======================== 3. THREAT SCORE FUNCTION ========================
def compute_threat_score(password_ok, answer_ok, amount_ok):
    """
    password_ok: True if password matches
    answer_ok: True if personal answer matches
    amount_ok: True if withdrawal amount <= user's limit
    Returns a score between 0 and 1
    """
    score = 0.0
    if not password_ok:
        score += 0.6
    if not answer_ok:
        score += 0.5
    if not amount_ok:
        score += 0.3
    return min(score, 1.0)

# ======================== 4. DECISION FUNCTION ========================
def make_decision(score):
    if score > 0.8:
        return "BLOCKED", "HIGH RISK - Transaction blocked"
    elif score >= 0.5:
        return "FLAGGED", "MEDIUM RISK - Requires human analyst review"
    else:
        return "ALLOWED", "LOW RISK - Transaction approved"

# ======================== 5. MAIN PROGRAM ========================
print("="*50)
print(" AI-POWERED BANKING SECURITY SYSTEM")
print("="*50)

# Show available users
print("\n Available users:")
for name in users.keys():
    print(f"   - {name}")

user_name = input("\n Enter your full name: ").strip()

if user_name not in users:
    print(" User not found! Access denied.")
    exit()

user_data = users[user_name]
print(f"\n Welcome, {user_name}!")

# Step 1: Password
password = input(" Enter your password: ").strip()
password_ok = (password == user_data["password"])

# Step 2: Personal question
print(f"\n Personal verification: {user_data['question']}")
answer = input("Your answer: ").strip()
answer_ok = (answer.lower() == user_data["answer"].lower())

# Step 3: Withdrawal amount
try:
    amount = float(input(f"\n Enter amount to withdraw (INR): "))
    amount_ok = (amount <= user_data["limit"])
except:
    amount_ok = False
    amount = 0

# Compute threat score
score = compute_threat_score(password_ok, answer_ok, amount_ok)
decision, short_msg = make_decision(score)

# Display result
print("\n" + "="*50)
print(f" THREAT SCORE: {score:.2f}")
print(f" DECISION: {decision}")
print(f" {short_msg}")
print("="*50)

# Send email alert if score > 0.8 (BLOCKED) or score >= 0.5 (FLAGGED)
if score > 0.8 or score >= 0.5:
    send_alert_simulation(
        customer_name=user_name,
        customer_email=user_data["email"],
        amount=amount,
        score=score,
        decision=decision,
        message=short_msg
    )
else:
    print("\n No alert needed. Transaction allowed.")

# ======================== 6. SAVE TO DATASET (bank_logs.csv) ========================
log_entry = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "user": user_name,
    "password_ok": password_ok,
    "answer_ok": answer_ok,
    "amount_requested": amount,
    "user_limit": user_data["limit"],
    "amount_within_limit": amount_ok,
    "threat_score": round(score, 2),
    "decision": decision,
    "alert_message": short_msg
}

new_entry_df = pd.DataFrame([log_entry])

if os.path.exists("bank_logs.csv"):
    existing = pd.read_csv("bank_logs.csv")
    updated = pd.concat([existing, new_entry_df], ignore_index=True)
else:
    updated = new_entry_df

updated.to_csv("bank_logs.csv", index=False)
print("\n Log saved to bank_logs.csv")

# ======================== 7. DASHBOARD: PIE CHART ========================
if os.path.exists("bank_logs.csv"):
    logs = pd.read_csv("bank_logs.csv")
    risk_counts = logs["decision"].value_counts()
    
    plt.figure(figsize=(6,6))
    colors_map = {"ALLOWED": "green", "FLAGGED": "orange", "BLOCKED": "red"}
    colors = [colors_map.get(decision, "gray") for decision in risk_counts.index]
    plt.pie(risk_counts, labels=risk_counts.index, autopct="%1.1f%%", startangle=90, colors=colors)
    plt.title("Risk Decision Distribution (All Transactions)")
    plt.savefig("risk_dashboard.png")
    plt.show()
    print("\n Pie chart saved as 'risk_dashboard.png'")
else:
    print("\nNo logs yet. Run more transactions to see pie chart.")

print("\n System execution complete.")
