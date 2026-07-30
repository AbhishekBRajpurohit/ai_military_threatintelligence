"""
train_attack_model.py
----------------------
Trains a classification model to predict Attack Type using the
Global Terrorism Database (GTD) dataset.

Run this ONCE to generate:
  - models/attack_prediction_model.pkl
  - models/feature_encoders.pkl
  - models/target_encoder.pkl
  - models/model_metrics.json
"""

import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

DATA_PATH = "data/globalterrorism.csv"

print("Loading dataset...")
df = pd.read_csv(DATA_PATH, encoding="latin-1", low_memory=False)

columns_needed = [
    "country_txt", "region_txt", "gname", "success", "suicide",
    "weaptype1_txt", "targtype1_txt", "nkill", "nwound", "attacktype1_txt"
]

df = df[columns_needed].copy()

df["nkill"] = df["nkill"].fillna(0)
df["nwound"] = df["nwound"].fillna(0)
df = df.dropna(subset=["gname", "weaptype1_txt", "targtype1_txt", "attacktype1_txt"])

top_groups = df["gname"].value_counts().nlargest(50).index
df["gname"] = df["gname"].apply(lambda x: x if x in top_groups else "Unknown")

categorical_cols = ["country_txt", "region_txt", "gname", "weaptype1_txt", "targtype1_txt"]
encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    encoders[col] = le

target_encoder = LabelEncoder()
df["attacktype1_txt"] = target_encoder.fit_transform(df["attacktype1_txt"].astype(str))

feature_cols = [
    "country_txt", "region_txt", "gname", "success",
    "suicide", "weaptype1_txt", "targtype1_txt", "nkill", "nwound"
]

X = df[feature_cols]
y = df["attacktype1_txt"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Training RandomForest model...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {acc*100:.2f}%\n")

report_dict = classification_report(
    y_test, y_pred, target_names=target_encoder.classes_,
    zero_division=0, output_dict=True
)
print(classification_report(y_test, y_pred, target_names=target_encoder.classes_, zero_division=0))

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/attack_prediction_model.pkl", compress=3)
joblib.dump(encoders, "models/feature_encoders.pkl")
joblib.dump(target_encoder, "models/target_encoder.pkl")

metrics = {
    "accuracy": acc,
    "n_train": len(X_train),
    "n_test": len(X_test),
    "report": report_dict,
}
with open("models/model_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("\nSaved model, encoders, and metrics to /models folder.")