import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from auth import check_password

if not check_password():
    st.stop()

st.set_page_config(page_title="Group Profile", page_icon="🕵️", layout="wide")
st.title("🕵️ Terrorist Group Profile")

df = load_data()

groups = sorted(df["gname"].dropna().unique().tolist())
groups = [g for g in groups if g != "Unknown"]
selected_group = st.selectbox("Select Group", groups)

gdf = df[df["gname"] == selected_group]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Incidents", len(gdf))
c2.metric("Fatalities", int(gdf["nkill"].sum()))
c3.metric("Countries Active In", gdf["country_txt"].nunique())
c4.metric("Active Years", f"{int(gdf['iyear'].min())}–{int(gdf['iyear'].max())}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    trend = gdf.groupby("iyear", observed=True).size().reset_index(name="Attacks")
    fig1 = px.line(trend, x="iyear", y="Attacks", markers=True, title="Activity Over Time")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    weapons = gdf["weaptype1_txt"].value_counts().head(8).reset_index()
    weapons.columns = ["Weapon", "Count"]
    fig2 = px.bar(weapons, x="Count", y="Weapon", orientation="h", title="Preferred Weapons")
    st.plotly_chart(fig2, use_container_width=True)

top_countries = gdf["country_txt"].value_counts().head(10).reset_index()
top_countries.columns = ["Country", "Attacks"]
fig3 = px.bar(top_countries, x="Country", y="Attacks", title="Top Countries Targeted")
st.plotly_chart(fig3, use_container_width=True)

st.divider()

st.subheader("Recent Incidents")
recent = gdf.sort_values("iyear", ascending=False)[
    ["iyear", "country_txt", "city", "attacktype1_txt", "nkill", "nwound"]
].head(20)
recent.columns = ["Year", "Country", "City", "Attack Type", "Killed", "Wounded"]
st.dataframe(recent, use_container_width=True)