"""
train_attack_model.py
----------------------
Trains a classification model to predict Attack Type using the
Global Terrorism Database (GTD) dataset.

Uses a TIME-BASED split (train on earlier years, test on later years)
instead of a random split — this is more honest for a temporal dataset,
since a random split lets future patterns leak into training.

Run this ONCE to generate:
  - models/attack_prediction_model.pkl
  - models/feature_encoders.pkl
  - models/target_encoder.pkl
  - models/model_metrics.json
"""

import pandas as pd
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

DATA_PATH = "data/globalterrorism.csv"
TEST_YEARS_FRACTION = 0.2

print("Loading dataset...")
df = pd.read_csv(DATA_PATH, encoding="latin-1", low_memory=False)

columns_needed = [
    "iyear", "country_txt", "region_txt", "gname", "success", "suicide",
    "weaptype1_txt", "targtype1_txt", "attacktype1_txt"
]

df = df[columns_needed].copy()
df = df.dropna(subset=["gname", "weaptype1_txt", "targtype1_txt", "attacktype1_txt", "iyear"])

top_groups = df["gname"].value_counts().nlargest(50).index
df["gname"] = df["gname"].apply(lambda x: x if x in top_groups else "Unknown")

df = df.sort_values("iyear")
split_index = int(len(df) * (1 - TEST_YEARS_FRACTION))
split_year = df.iloc[split_index]["iyear"]

print(f"Splitting at year {split_year}: train = years before it, test = years from it onward.")

train_df = df[df["iyear"] < split_year].copy()
test_df = df[df["iyear"] >= split_year].copy()

print(f"Train rows: {len(train_df):,} | Test rows: {len(test_df):,}")

categorical_cols = ["country_txt", "region_txt", "gname", "weaptype1_txt", "targtype1_txt"]
encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    le.fit(train_df[col].astype(str))
    encoders[col] = le

    known_classes = set(le.classes_)
    train_df[col] = le.transform(train_df[col].astype(str))
    test_df[col] = test_df[col].astype(str).apply(
        lambda x: x if x in known_classes else le.classes_[0]
    )
    test_df[col] = le.transform(test_df[col])

target_encoder = LabelEncoder()
target_encoder.fit(train_df["attacktype1_txt"].astype(str))
known_targets = set(target_encoder.classes_)

train_df["attacktype1_txt"] = target_encoder.transform(train_df["attacktype1_txt"].astype(str))
test_df = test_df[test_df["attacktype1_txt"].astype(str).isin(known_targets)]
test_df["attacktype1_txt"] = target_encoder.transform(test_df["attacktype1_txt"].astype(str))

feature_cols = ["country_txt", "region_txt", "gname", "success", "suicide",
                "weaptype1_txt", "targtype1_txt"]

X_train, y_train = train_df[feature_cols], train_df["attacktype1_txt"]
X_test, y_test = test_df[feature_cols], test_df["attacktype1_txt"]

print("Training RandomForest model...")
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=15,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy (on future/unseen years): {acc*100:.2f}%\n")

present_labels = sorted(set(y_test) | set(y_pred))
present_names = target_encoder.inverse_transform(present_labels)

report_dict = classification_report(
    y_test, y_pred, labels=present_labels, target_names=present_names,
    zero_division=0, output_dict=True
)
print(classification_report(y_test, y_pred, labels=present_labels,
                             target_names=present_names, zero_division=0))

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/attack_prediction_model.pkl", compress=3)
joblib.dump(encoders, "models/feature_encoders.pkl")
joblib.dump(target_encoder, "models/target_encoder.pkl")

metrics = {
    "accuracy": acc,
    "split_type": "temporal",
    "split_year": int(split_year),
    "n_train": len(X_train),
    "n_test": len(X_test),
    "report": report_dict,
}
with open("models/model_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("\nSaved model, encoders, and metrics to /models folder.")