import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.title("🌍 Country Analysis")

# Load dataset
df = load_data()

# -----------------------------
# Country Selection
# -----------------------------
countries = sorted(df["country_txt"].dropna().unique())

selected_country = st.selectbox(
    "Select Country",
    countries
)

country_df = df[df["country_txt"] == selected_country]

# -----------------------------
# Summary Metrics
# -----------------------------
st.subheader(f"📊 {selected_country} Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Incidents", len(country_df))
c2.metric("Fatalities", int(country_df["nkill"].fillna(0).sum()))
c3.metric("Injured", int(country_df["nwound"].fillna(0).sum()))
c4.metric("Cities", country_df["city"].nunique())

st.divider()

# -----------------------------
# Attacks Over Years
# -----------------------------
st.subheader("📈 Attacks Over Years")

year_df = (
    country_df.groupby("iyear")
    .size()
    .reset_index(name="Attacks")
)

fig = px.line(
    year_df,
    x="iyear",
    y="Attacks",
    markers=True,
    title=f"Attacks in {selected_country}"
)

fig.update_layout(xaxis_title="Year", yaxis_title="Number of Attacks")

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Attack Type Distribution
# -----------------------------
st.subheader("🎯 Attack Types")

attack_df = (
    country_df["attacktype1_txt"]
    .value_counts()
    .reset_index()
)

attack_df.columns = ["Attack Type", "Count"]

fig2 = px.bar(
    attack_df,
    x="Attack Type",
    y="Count",
    color="Count",
    title="Attack Type Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Top Terrorist Groups
# -----------------------------
st.subheader("👥 Top Terrorist Groups")

group_df = (
    country_df["gname"]
    .value_counts()
    .head(10)
    .reset_index()
)

group_df.columns = ["Group", "Incidents"]

fig3 = px.bar(
    group_df,
    x="Incidents",
    y="Group",
    orientation="h",
    color="Incidents",
    title="Top 10 Terrorist Groups"
)

fig3.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Fatalities Over Years
# -----------------------------
st.subheader("💥 Fatalities Over Years")

fatal_df = (
    country_df.groupby("iyear")["nkill"]
    .sum()
    .fillna(0)
    .reset_index()
)

fig4 = px.line(
    fatal_df,
    x="iyear",
    y="nkill",
    markers=True,
    title="Fatalities by Year"
)

fig4.update_layout(
    xaxis_title="Year",
    yaxis_title="Fatalities"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Top Affected Cities
# -----------------------------
st.subheader("🏙️ Top Affected Cities")

city_df = (
    country_df[
        country_df["city"].notna() &
        (country_df["city"] != "Unknown")
    ]["city"]
    .value_counts()
    .head(10)
    .reset_index()
)

city_df.columns = ["City", "Incidents"]

fig5 = px.bar(
    city_df,
    x="City",
    y="Incidents",
    color="Incidents",
    title="Top 10 Affected Cities"
)

st.plotly_chart(fig5, use_container_width=True)

st.success(f"Analysis completed for {selected_country}.")