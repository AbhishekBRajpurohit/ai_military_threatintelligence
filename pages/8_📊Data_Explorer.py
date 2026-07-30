import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(page_title="Data Explorer", page_icon="📊", layout="wide")
st.title("📊 Data Explorer")
st.write("Filter, explore, and visualize the raw incident data.")

df = load_data()

st.sidebar.header("🔍 Filters")

year_min, year_max = int(df["iyear"].min()), int(df["iyear"].max())
year_range = st.sidebar.slider("Year Range", year_min, year_max, (year_min, year_max))

countries = st.sidebar.multiselect(
    "Country", sorted(df["country_txt"].dropna().unique().tolist())
)

attack_types = st.sidebar.multiselect(
    "Attack Type", sorted(df["attacktype1_txt"].dropna().unique().tolist())
)

filtered = df[(df["iyear"] >= year_range[0]) & (df["iyear"] <= year_range[1])]

if countries:
    filtered = filtered[filtered["country_txt"].isin(countries)]

if attack_types:
    filtered = filtered[filtered["attacktype1_txt"].isin(attack_types)]

st.subheader(f"Showing {len(filtered):,} incidents")

st.dataframe(filtered, use_container_width=True, height=400)

st.download_button(
    "⬇️ Download filtered data (CSV)",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_data.csv",
    mime="text/csv"
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    yearly = filtered.groupby("iyear").size().reset_index(name="Attacks")
    fig1 = px.bar(yearly, x="iyear", y="Attacks", title="Attacks by Year")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    region_counts = filtered["region_txt"].value_counts().reset_index()
    region_counts.columns = ["Region", "Attacks"]
    fig2 = px.bar(region_counts, x="Attacks", y="Region", orientation="h", title="Attacks by Region")
    fig2.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig2, use_container_width=True)