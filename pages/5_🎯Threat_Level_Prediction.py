import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
from config import SEVERITY_MODEL_PATH, SEVERITY_ENCODERS_PATH
from utils.auth_ui import require_login

require_login()

st.set_page_config(page_title="Threat Level Prediction", page_icon="🎯", layout="wide")
st.title("🎯 Threat Level Prediction")
st.write("Estimate the overall threat level of an incident based on its characteristics.")

col1, col2 = st.columns(2)

with col1:
    nkill = st.number_input("☠️ Number of Fatalities", min_value=0, value=0, step=1)
    nwound = st.number_input("🚑 Number of Injured", min_value=0, value=0, step=1)
    suicide = st.selectbox("💣 Suicide Attack?", ["No", "Yes"])

with col2:
    success = st.selectbox("✅ Attack Successful?", ["Yes", "No"])
    weapon_type = st.selectbox(
        "🔫 Weapon Type",
        ["Firearms", "Explosives", "Incendiary", "Chemical", "Biological",
         "Melee", "Sabotage Equipment", "Unknown", "Other"]
    )
    target_type = st.selectbox(
        "🎯 Target Type",
        ["Private Citizens & Property", "Government (General)", "Military",
         "Police", "Business", "Educational Institution", "Religious Figures/Institutions",
         "Transportation", "Other"]
    )

predict_btn = st.button("🚨 Assess Threat Level")

WEAPON_WEIGHTS = {
    "Chemical": 25, "Biological": 25, "Explosives": 20, "Incendiary": 15,
    "Firearms": 12, "Sabotage Equipment": 10, "Melee": 6, "Unknown": 5, "Other": 8
}

HIGH_VALUE_TARGETS = {
    "Government (General)", "Military", "Police",
    "Religious Figures/Institutions", "Transportation"
}


def compute_threat_score(nkill, nwound, suicide, success, weapon_type, target_type):
    score = 0
    score += min(nkill * 4, 40)
    score += min(nwound * 1.5, 20)
    score += WEAPON_WEIGHTS.get(weapon_type, 5)
    score += 15 if suicide == "Yes" else 0
    score += 10 if success == "Yes" else 0
    score += 10 if target_type in HIGH_VALUE_TARGETS else 3
    return min(round(score), 100)


def score_to_level(score):
    if score < 25:
        return "Low", "#2ecc71"
    elif score < 50:
        return "Moderate", "#f1c40f"
    elif score < 75:
        return "High", "#e67e22"
    else:
        return "Critical", "#e74c3c"


@st.cache_resource
def load_severity_model():
    model = joblib.load(SEVERITY_MODEL_PATH)
    encoders = joblib.load(SEVERITY_ENCODERS_PATH)
    return model, encoders


if predict_btn:
    score = compute_threat_score(nkill, nwound, suicide, success, weapon_type, target_type)
    level, color = score_to_level(score)

    st.markdown(
        f"### Predicted Threat Level: "
        f"**:{'green' if level == 'Low' else 'orange' if level in ['Moderate', 'High'] else 'red'}[{level}]**"
    )

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Threat Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 25], "color": "#eafaf1"},
                {"range": [25, 50], "color": "#fef9e7"},
                {"range": [50, 75], "color": "#fdebd0"},
                {"range": [75, 100], "color": "#fadbd8"},
            ],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "This score is a heuristic (rule-based) estimate combining casualty impact, "
        "weapon severity, target sensitivity, and attack characteristics. "
        "It is intended for educational/analytical demonstration, not operational use."
    )

    st.divider()
    st.subheader("🤖 ML-Based Casualty Estimate")

    try:
        sev_model, sev_encoders = load_severity_model()

        input_row = pd.DataFrame({
            "country_txt": [0],
            "region_txt": [0],
            "attacktype1_txt": [0],
            "weaptype1_txt": [sev_encoders["weaptype1_txt"].transform([weapon_type])[0]
                              if weapon_type in sev_encoders["weaptype1_txt"].classes_ else 0],
            "targtype1_txt": [sev_encoders["targtype1_txt"].transform([target_type])[0]
                              if target_type in sev_encoders["targtype1_txt"].classes_ else 0],
            "suicide": [1 if suicide == "Yes" else 0],
            "success": [1 if success == "Yes" else 0],
        })

        ml_estimate = sev_model.predict(input_row)[0]
        st.metric("ML-Estimated Casualties (nkill + nwound)", f"{ml_estimate:.1f}")
        st.caption(
            "Predicted from historical patterns using a RandomForest regressor. "
            "Country/region are not set from this form, so treat this as a rough baseline."
        )

    except FileNotFoundError:
        st.caption("Run `train_severity_model.py` to enable ML-based casualty estimation here.")