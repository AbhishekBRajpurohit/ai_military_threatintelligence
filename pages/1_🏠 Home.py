import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.title("🏠 Home")

df = load_data()

# ===============================
# Dashboard Summary
# ===============================

st.subheader("Dashboard Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Incidents", len(df))
c2.metric("Fatalities", int(df["nkill"].sum()))
c3.metric("Injured", int(df["nwound"].sum()))
c4.metric("Countries", df["country_txt"].nunique())

st.divider()

# ===============================
# Attacks Over Years
# ===============================

st.subheader("Attacks Over Years")

yearly = (
    df.groupby("iyear")
      .size()
      .reset_index(name="Attacks")
)

fig = px.line(
    yearly,
    x="iyear",
    y="Attacks",
    markers=True,
    title=""
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Attacks",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.success(
    "👉 Click **Global Threat Map** from the left sidebar to explore incidents geographically."
)