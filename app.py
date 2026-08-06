import streamlit as st
from utils.auth_ui import require_login

st.set_page_config(
    page_title="GTD Analytical Dashboard",
    page_icon="🛡️",
    layout="wide"
)

require_login()

st.title("🛡️ GTD Analytics & Forecasting Dashboard")

st.markdown("""
### Welcome to app

This dashboard provides analytics on the Global Terrorism Database (GTD) —
a public historical research dataset. It is intended for educational and
analytical demonstration purposes.

👉 Select a page from the sidebar.
""")

st.info("""
Available Modules

- 🏠 Home
- 🌍 Global Threat Map
- 🌍 Country Analysis
- ⚖️ Compare Countries
- 🤖 Attack Prediction
- 🎯 Threat Level Prediction
- 📈 Forecasting
- 🧠 AI Intelligence Report
- 📊 Data Explorer
- 🕵️ Group Profile
- ⚙️ Settings

👉 Use the **left sidebar** to navigate.
""")

st.caption(
    "⚠️ This is a research/educational tool built on public historical data. "
    "It is not connected to any live intelligence source and should not be "
    "used for operational decision-making."
)