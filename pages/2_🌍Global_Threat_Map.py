import streamlit as st
import plotly.express as px
import folium
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium
from utils.data_loader import load_data
from utils.auth_ui import require_login

require_login()

st.title("🌍 Global Threat Map")

df = load_data()

st.sidebar.header("Filters")

years = ["All"] + sorted(df["iyear"].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("Year", years)

regions = ["All"] + sorted(df["region_txt"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Region", regions)

attack_types = ["All"] + sorted(df["attacktype1_txt"].dropna().unique().tolist())
selected_attack = st.sidebar.selectbox("Attack Type", attack_types)

filtered_df = df

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["iyear"] == selected_year]

if selected_region !=