# src/train_model.py
# Train Random Forest on NSL-KDD dataset for network intrusion detection

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report
import joblib
import urllib.request
import os

print("Downloading NSL-KDD dataset...")
url = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt"
if not os.path.exists("data/KDDTrain.csv"):
    os.makedirs("data", exist_ok=True)
    urllib.request.urlretrieve(url, "data/KDDTrain.csv")

# Define column names (41 features + 1 label)
columns = [
    "duration",
    "protocol_type",
    "service",
    "flag",
    "src_bytes",
    "dst_bytes",
    "land",
    "wrong_fragment",
    "urgent",
    "hot",
    "num_failed_logins",
    "logged_in",
    "num_compromised",
    "root_shell",
    "su_attempted",
    "num_root",
    "num_file_creations",
    "num_shells",
    "num_access_files",
    "num_outbound_cmds",
    "is_host_login",
    "is_guest_login",
    "count",
    "srv_count",
    "serror_rate",
    "srv_serror_rate",
    "rerror_rate",
    "srv_rerror_rate",
    "same_srv_rate",
    "diff_srv_rate",
    "srv_diff_host_rate",
    "dst_host_count",
    "dst_host_srv_count",
    "dst_host_same_srv_rate",
    "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate",
    "dst_host_srv_serror_rate",
    "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate",
    "attack_type",
    "difficulty_level",
]

df = pd.read_csv("data/KDDTrain.csv", header=None, names=columns)

# Simplify labels: 0 = normal, 1 = attack
df["label"] = df["attack_type"].apply(lambda x: 0 if x == "normal." else 1)

# Features and target
X = df.drop(["attack_type", "difficulty_level", "label"], axis=1)
y = df["label"]

# Encode categorical features
categorical_cols = X.select_dtypes(include=["object"]).columns
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Train Random Forest
print("Training Random Forest...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model and scaler
joblib.dump(model, "cybersecurity_model.pkl")
joblib.dump(scaler, "scaler.pkl")
print("Model saved as 'cybersecurity_model.pkl' and scaler saved as 'scaler.pkl'")
