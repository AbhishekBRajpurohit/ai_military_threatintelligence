import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
st.title("⚙️ Settings")

# ---------------------------------------------------------
# Dataset info
# ---------------------------------------------------------
st.subheader("📁 Dataset Information")

data_path = "data/globalterrorism.csv"

if os.path.exists(data_path):
    file_size = os.path.getsize(data_path) / (1024 * 1024)
    df = pd.read_csv(data_path, encoding="latin-1", low_memory=False)

    col1, col2, col3 = st.columns(3)
    col1.metric("File Size", f"{file_size:.2f} MB")
    col2.metric("Total Rows", f"{len(df):,}")
    col3.metric("Total Columns", f"{len(df.columns)}")

    with st.expander("View column names"):
        st.write(list(df.columns))
else:
    st.error("Dataset not found at data/globalterrorism.csv")

st.markdown("---")

# ---------------------------------------------------------
# Model info
# ---------------------------------------------------------
st.subheader("🤖 Model Status")

model_files = {
    "Attack Prediction Model": "models/attack_prediction_model.pkl",
    "Feature Encoders": "models/feature_encoders.pkl",
    "Target Encoder": "models/target_encoder.pkl",
}

for name, path in model_files.items():
    if os.path.exists(path):
        size_kb = os.path.getsize(path) / 1024
        st.success(f"✅ {name} — found ({size_kb:.1f} KB)")
    else:
        st.warning(f"⚠️ {name} — not found. Run train_attack_model.py to generate it.")

st.markdown("---")

# ---------------------------------------------------------
# Cache management
# ---------------------------------------------------------
st.subheader("🧹 Cache Management")
st.write("If you've retrained the model or updated the dataset, clear the cache below and reload the app.")

if st.button("Clear Cache"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.success("Cache cleared! Please refresh the page.")

st.markdown("---")

# ---------------------------------------------------------
# About
# ---------------------------------------------------------
st.subheader("ℹ️ About This Dashboard")
st.markdown("""
**AI-Based Military Intelligence Dashboard**

Built using the Global Terrorism Database (GTD) for academic and analytical purposes.

**Tech Stack:** Streamlit · Pandas · Scikit-learn · Prophet · Plotly · Folium

**Modules:**
- Global Threat Map
- Country Analysis
- Attack Type Prediction (ML)
- Threat Level Assessment
- Time-Series Forecasting
- AI Intelligence Report Generation
- Interactive Data Explorer

*This project is intended for educational and research purposes only.*
""")
