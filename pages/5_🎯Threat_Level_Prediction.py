import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Threat Level Prediction", page_icon="🎯", layout="wide")
st.title("🎯 Threat Level Prediction")
st.write("Estimate the overall threat level of an incident based on its characteristics.")

# ---------------------------------------------------------
# Input form
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# Rule-based scoring engine
# ---------------------------------------------------------
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
    score += min(nkill * 4, 40)          # casualties weigh heavily, capped
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

# ---------------------------------------------------------
# Output
# ---------------------------------------------------------
if predict_btn:
    score = compute_threat_score(nkill, nwound, suicide, success, weapon_type, target_type)
    level, color = score_to_level(score)

    st.markdown(f"### Predicted Threat Level: **:{'green' if level=='Low' else 'orange' if level in ['Moderate','High'] else 'red'}[{level}]**")

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
