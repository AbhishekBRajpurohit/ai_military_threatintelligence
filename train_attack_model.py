"""
train_attack_model.py
----------------------
Trains a classification model to predict Attack Type using the
Global Terrorism Database (GTD) dataset from Kaggle.

Run this ONCE to generate:
  - models/attack_prediction_model.pkl
  - models/feature_encoders.pkl
  - models/target_encoder.pkl

Make sure your dataset CSV (globalterrorism.csv) is placed inside data/
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# ---------------------------------------------------------
# 1. Load Dataset
# ---------------------------------------------------------
DATA_PATH = "data/globalterrorism.csv"

print("Loading dataset...")
df = pd.read_csv(DATA_PATH, encoding="latin-1", low_memory=False)

# ---------------------------------------------------------
# 2. Select relevant columns
# (These are the standard GTD column names on Kaggle)
# ---------------------------------------------------------
columns_needed = [
    "country_txt",      # Country
    "region_txt",        # Region
    "gname",              # Terrorist Group
    "success",            # Attack Successful? (1/0)
    "suicide",            # Suicide Attack? (1/0)
    "weaptype1_txt",     # Weapon Type
    "targtype1_txt",     # Target Type
    "nkill",               # Number of Fatalities
    "nwound",             # Number of Injured
    "attacktype1_txt"    # TARGET: Attack Type
]

df = df[columns_needed].copy()

# ---------------------------------------------------------
# 3. Clean data
# ---------------------------------------------------------
df["nkill"] = df["nkill"].fillna(0)
df["nwound"] = df["nwound"].fillna(0)
df = df.dropna(subset=["gname", "weaptype1_txt", "targtype1_txt", "attacktype1_txt"])

# Limit terrorist groups to top 50 most frequent (avoids huge sparse encoding)
top_groups = df["gname"].value_counts().nlargest(50).index
df["gname"] = df["gname"].apply(lambda x: x if x in top_groups else "Unknown")

# ---------------------------------------------------------
# 4. Encode categorical columns
# ---------------------------------------------------------
categorical_cols = ["country_txt", "region_txt", "gname", "weaptype1_txt", "targtype1_txt"]
encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    encoders[col] = le

# Encode target
target_encoder = LabelEncoder()
df["attacktype1_txt"] = target_encoder.fit_transform(df["attacktype1_txt"].astype(str))

# ---------------------------------------------------------
# 5. Prepare features (X) and target (y)
# ---------------------------------------------------------
feature_cols = [
    "country_txt", "region_txt", "gname", "success",
    "suicide", "weaptype1_txt", "targtype1_txt", "nkill", "nwound"
]

X = df[feature_cols]
y = df["attacktype1_txt"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------------------------------------
# 6. Train model
# ---------------------------------------------------------
print("Training RandomForest model...")
model = RandomForestClassifier(
    n_estimators=100,      # was 200
    max_depth=15,          # was 20
    min_samples_leaf=5,    # NEW — reduces tree size significantly
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)
model.fit(X_train, y_train)

# ---------------------------------------------------------
# 7. Evaluate
# ---------------------------------------------------------
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {acc*100:.2f}%\n")
print(classification_report(y_test, y_pred, target_names=target_encoder.classes_, zero_division=0))

# ---------------------------------------------------------
# 8. Save model + encoders
# ---------------------------------------------------------
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/attack_prediction_model.pkl", compress=3)
joblib.dump(encoders, "models/feature_encoders.pkl")
joblib.dump(target_encoder, "models/target_encoder.pkl")

print("\nSaved model and encoders to /models folder.")