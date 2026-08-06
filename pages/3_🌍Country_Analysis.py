import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.auth_ui import require_login

require_login()

st.title("🌍 Country Analysis")

df = load_data()

countries = sorted(df["country_txt"].dropna().unique())
selected_country = st.selectbox("Select Country", countries)

country_df = df[df["country_txt"] == selected_country]

st.subheader(f"📊 {selected_country} Summary")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Incidents", len(country_df))
c2.metric("Fatalities", int(country_df["nkill"].sum()))
c3.metric("Injured", int(country_df["nwound"].sum()))
c4.metric("Cities", country_df["city"].nunique())

st.divider()

st.subheader("📈 Attacks Over Years estimated ")

year_df = country_df.groupby("iyear", observed=True).size().reset_index(name="Attacks")

fig = px.line(
    year_df, x="iyear", y="Attacks", markers=True,
    title=f"Attacks in {selected_country}"
)
fig.update_layout(xaxis_title="Year", yaxis_title="Number of Attacks")
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("🎯 Attack Type Distribution")

attack_dist = country_df["attacktype1_txt"].value_counts().reset_index()
attack_dist.columns = ["Attack Type", "Count"]

fig2 = px.pie(attack_dist, names="Attack Type", values="Count", hole=0.4)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("🔫 Weapon Type Breakdown")

weapon_dist = country_df["weaptype1_txt"].value_counts().head(10).reset_index()
weapon_dist.columns = ["Weapon", "Count"]

fig3 = px.bar(
    weapon_dist, x="Count", y="Weapon", orientation="h",
    title="Top Weapons Used", color="Count", color_continuous_scale="Reds"
)
fig3.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig3, use_container_width=True)

st.divider()

st.subheader("👥 Groups Active in this Country")

group_dist = country_df["gname"].value_counts().head(10).reset_index()
group_dist.columns = ["Group", "Attacks"]
st.dataframe(group_dist, use_container_width=True)