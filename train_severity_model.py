"""
train_severity_model.py
------------------------
Trains a regression model to predict expected casualties (nkill + nwound)
as an ML-based complement to the rule-based Threat Level page.
"""

import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

DATA_PATH = "data/globalterrorism.csv"

df = pd.read_csv(DATA_PATH, encoding="latin-1", low_memory=False)

cols = ["country_txt", "region_txt", "attacktype1_txt", "weaptype1_txt",
        "targtype1_txt", "suicide", "success", "nkill", "nwound"]
df = df[cols].dropna(subset=["attacktype1_txt", "weaptype1_txt", "targtype1_txt"])
df["nkill"] = df["nkill"].fillna(0)
df["nwound"] = df["nwound"].fillna(0)
df["severity"] = df["nkill"] + df["nwound"]

cat_cols = ["country_txt", "region_txt", "attacktype1_txt", "weaptype1_txt", "targtype1_txt"]
encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    encoders[col] = le

feature_cols = cat_cols + ["suicide", "success"]
X = df[feature_cols]
y = df["severity"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training RandomForest regressor...")
model = RandomForestRegressor(
    n_estimators=150, max_depth=12, min_samples_leaf=5,
    random_state=42, n_jobs=-1
)
model.fit(X_train, y_train)

pred = model.predict(X_test)
print(f"MAE: {mean_absolute_error(y_test, pred):.2f}")
print(f"R2: {r2_score(y_test, pred):.3f}")

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/severity_model.pkl", compress=3)
joblib.dump(encoders, "models/severity_encoders.pkl")
print("Saved severity model and encoders to /models folder.")