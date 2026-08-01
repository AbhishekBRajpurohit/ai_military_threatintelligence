import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
from config import ATTACK_MODEL_PATH, FEATURE_ENCODERS_PATH, TARGET_ENCODER_PATH

st.set_page_config(page_title="Attack Prediction", page_icon="🤖", layout="wide")
st.title("🤖 Attack Type Prediction")
st.write("Enter the incident details below and click **Predict Attack Type**.")
st.caption(
    "This model predicts attack type using only information known *before* an "
    "attack occurs (location, group, weapon/target choice) — casualty counts are "
    "excluded since those are outcomes, not predictors."
)


@st.cache_resource
def load_model_and_encoders():
    t0 = time.time()
    model = joblib.load(ATTACK_MODEL_PATH)
    encoders = joblib.load(FEATURE_ENCODERS_PATH)
    target_encoder = joblib.load(TARGET_ENCODER_PATH)
    print(f"[Attack Prediction] Model load took {time.time() - t0:.2f}s")
    return model, encoders, target_encoder


model_loaded = False
try:
    with st.spinner("Loading model (first load only — cached after)..."):
        model, encoders, target_encoder = load_model_and_encoders()
    model_loaded = True
except FileNotFoundError as e:
    st.error(
        f"Model file missing: {e}\n\n"
        "Run `python train_attack_model.py` first to generate the model and encoder files."
    )
except Exception as e:
    st.error(f"Failed to load model ({type(e).__name__}): {e}")

if model_loaded:
    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox("🌍 Country", sorted(encoders["country_txt"].classes_))
        region = st.selectbox("🌍 Region", sorted(encoders["region_txt"].classes_))
        weapon_type = st.selectbox("🔫 Weapon Type", sorted(encoders["weaptype1_txt"].classes_))
        target_type = st.selectbox("🎯 Target Type", sorted(encoders["targtype1_txt"].classes_))

    with col2:
        gname = st.selectbox("👥 Terrorist Group", sorted(encoders["gname"].classes_))
        success = st.selectbox("✅ Attack Successful?", ["Yes", "No"])
        suicide = st.selectbox("💣 Suicide Attack?", ["Yes", "No"])

    predict_btn = st.button("🚀 Predict Attack Type")

    if predict_btn:
        try:
            input_data = pd.DataFrame({
                "country_txt": [encoders["country_txt"].transform([country])[0]],
                "region_txt": [encoders["region_txt"].transform([region])[0]],
                "gname": [encoders["gname"].transform([gname])[0]],
                "success": [1 if success == "Yes" else 0],
                "suicide": [1 if suicide == "Yes" else 0],
                "weaptype1_txt": [encoders["weaptype1_txt"].transform([weapon_type])[0]],
                "targtype1_txt": [encoders["targtype1_txt"].transform([target_type])[0]],
            })

            prediction = model.predict(input_data)[0]
            probabilities = model.predict_proba(input_data)[0]
            confidence = np.max(probabilities) * 100

            predicted_label = target_encoder.inverse_transform([prediction])[0]

            st.success(f"Predicted Attack Type: **{predicted_label}**")

            st.subheader("Prediction Confidence")
            st.metric(label="Confidence", value=f"{confidence:.2f}%")

            with st.expander("See top predictions breakdown"):
                proba_df = pd.DataFrame({
                    "Attack Type": target_encoder.classes_,
                    "Probability (%)": probabilities * 100
                }).sort_values(by="Probability (%)", ascending=False).head(5)
                st.dataframe(proba_df, use_container_width=True)

        except Exception as e:
            st.error(f"Something went wrong during prediction: {e}")