import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ---------------------------------------------------------
# Page config
# ---------------------------------------------------------
st.set_page_config(page_title="Attack Prediction", page_icon="🤖", layout="wide")
st.title("🤖 Attack Type Prediction")
st.write("Enter the incident details below and click **Predict Attack Type**.")

# ---------------------------------------------------------
# Load model + encoders (cached so it only loads once)
# ---------------------------------------------------------
@st.cache_resource
def load_model_and_encoders():
    model = joblib.load("models/attack_prediction_model.pkl")
    encoders = joblib.load("models/feature_encoders.pkl")
    target_encoder = joblib.load("models/target_encoder.pkl")
    return model, encoders, target_encoder

try:
    model, encoders, target_encoder = load_model_and_encoders()
    model_loaded = True
except FileNotFoundError:
    model_loaded = False
    st.error(
        "Model files not found. Please run `train_attack_model.py` first "
        "to generate the model and encoder files inside the /models folder."
    )

# ---------------------------------------------------------
# Input form (matches your screenshot layout)
# ---------------------------------------------------------
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
        nkill = st.number_input("☠️ Number of Fatalities", min_value=0, value=0, step=1)
        nwound = st.number_input("🚑 Number of Injured", min_value=0, value=0, step=1)

    predict_btn = st.button("🚀 Predict Attack Type")

    # -------------------------------------------------------
    # Prediction logic
    # -------------------------------------------------------
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
                "nkill": [nkill],
                "nwound": [nwound],
            })

            prediction = model.predict(input_data)[0]
            probabilities = model.predict_proba(input_data)[0]
            confidence = np.max(probabilities) * 100

            predicted_label = target_encoder.inverse_transform([prediction])[0]

            st.success(f"Predicted Attack Type: **{predicted_label}**")

            st.subheader("Prediction Confidence")
            st.metric(label="Confidence", value=f"{confidence:.2f}%")

            # Optional: show top 3 probable classes
            with st.expander("See top predictions breakdown"):
                proba_df = pd.DataFrame({
                    "Attack Type": target_encoder.classes_,
                    "Probability (%)": probabilities * 100
                }).sort_values(by="Probability (%)", ascending=False).head(5)
                st.dataframe(proba_df, use_container_width=True)

        except Exception as e:
            st.error(f"Something went wrong during prediction: {e}")