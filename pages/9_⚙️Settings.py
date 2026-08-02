import streamlit as st
import pandas as pd
import json
import os
from config import DATA_PATH, ATTACK_MODEL_PATH, FEATURE_ENCODERS_PATH, TARGET_ENCODER_PATH, METRICS_PATH
from utils.data_loader import load_data
from auth import check_password

if not check_password():
    st.stop()

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
st.title("⚙️ Settings")

st.subheader("📁 Dataset Information")

if os.path.exists(DATA_PATH):
    file_size = os.path.getsize(DATA_PATH) / (1024 * 1024)
    df = load_data()

    col1, col2, col3 = st.columns(3)
    col1.metric("File Size", f"{file_size:.2f} MB")
    col2.metric("Total Rows", f"{len(df):,}")
    col3.metric("Total Columns", f"{len(df.columns)}")

    with st.expander("View column names"):
        st.write(list(df.columns))
else:
    st.error("Dataset not found at data/globalterrorism.csv")

st.markdown("---")

st.subheader("🤖 Model Status")

model_files = {
    "Attack Prediction Model": ATTACK_MODEL_PATH,
    "Feature Encoders": FEATURE_ENCODERS_PATH,
    "Target Encoder": TARGET_ENCODER_PATH,
}

for name, path in model_files.items():
    if os.path.exists(path):
        size_mb = os.path.getsize(path) / (1024 * 1024)
        st.write(f"**{name}**: ✅ Found — `{path}` ({size_mb:.2f} MB)")
    else:
        st.write(f"**{name}**: ❌ Missing — `{path}`")

st.markdown("---")

st.subheader("📈 Model Performance")

if os.path.exists(METRICS_PATH):
    with open(METRICS_PATH) as f:
        metrics = json.load(f)

    c1, c2, c3 = st.columns(3)
    c1.metric("Accuracy", f"{metrics['accuracy']*100:.2f}%")
    c2.metric("Train samples", f"{metrics['n_train']:,}")
    c3.metric("Test samples", f"{metrics['n_test']:,}")

    if metrics.get("split_type") == "temporal":
        st.caption(f"Evaluated with a temporal split — trained on years before {metrics.get('split_year')}, tested on years from {metrics.get('split_year')} onward.")

    with st.expander("Per-class precision / recall / F1"):
        report_df = pd.DataFrame(metrics["report"]).transpose()
        report_df = report_df[~report_df.index.isin(["accuracy", "macro avg", "weighted avg"])]
        st.dataframe(
            report_df.sort_values("support", ascending=False).round(3),
            use_container_width=True
        )
else:
    st.warning("No model_metrics.json found. Re-run train_attack_model.py to generate it.")