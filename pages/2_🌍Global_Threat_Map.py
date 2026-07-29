import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.title("🌍 Global Threat Map")

df = load_data()

# ==========================
# Sidebar Filters
# ==========================

st.sidebar.header("Filters")

# Year Filter
years = ["All"] + sorted(df["iyear"].dropna().unique().tolist())
selected_year = st.sidebar.selectbox(
    "Year",
    years
)

# Region Filter
regions = ["All"] + sorted(df["region_txt"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox(
    "Region",
    regions
)

# Attack Type Filter
attack_types = ["All"] + sorted(df["attacktype1_txt"].dropna().unique().tolist())
selected_attack = st.sidebar.selectbox(
    "Attack Type",
    attack_types
)

# ==========================
# Apply Filters
# ==========================

filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["iyear"] == selected_year
    ]

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["region_txt"] == selected_region
    ]

if selected_attack != "All":
    filtered_df = filtered_df[
        filtered_df["attacktype1_txt"] == selected_attack
    ]

# Remove missing coordinates
filtered_df = filtered_df.dropna(
    subset=["latitude", "longitude"]
)

# ==========================
# Global Threat Map
# ==========================

fig = px.scatter_geo(
    filtered_df,
    lat="latitude",
    lon="longitude",
    color="attacktype1_txt",
    hover_name="country_txt",
    hover_data={
        "city": True,
        "gname": True,
        "attacktype1_txt": True,
        "nkill": True,
        "latitude": False,
        "longitude": False,
    },
    projection="natural earth",
    height=700
)

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info("👉 Change filters from the sidebar.")