import streamlit as st
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from utils.data_loader import load_data

st.title("🌍 Global Threat Map")

df = load_data()

# ==========================
# Sidebar Filters
# ==========================
st.sidebar.header("Filters")

years = ["All"] + sorted(df["iyear"].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("Year", years)

regions = ["All"] + sorted(df["region_txt"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Region", regions)

attack_types = ["All"] + sorted(df["attacktype1_txt"].dropna().unique().tolist())
selected_attack = st.sidebar.selectbox("Attack Type", attack_types)

# ==========================
# Apply Filters
# ==========================
filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["iyear"] == selected_year]

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region_txt"] == selected_region]

if selected_attack != "All":
    filtered_df = filtered_df[filtered_df["attacktype1_txt"] == selected_attack]

filtered_df = filtered_df.dropna(subset=["latitude", "longitude"])

# ==========================
# Map (clustered if large, scatter_geo otherwise)
# ==========================
CLUSTER_THRESHOLD = 3000

if len(filtered_df) > CLUSTER_THRESHOLD:
    st.caption(f"Showing clustered view — {len(filtered_df):,} incidents match your filters.")

    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")
    cluster = MarkerCluster().add_to(m)

    for _, row in filtered_df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=3,
            popup=f"{row['country_txt']} — {row['attacktype1_txt']} ({int(row['nkill'])} killed)",
            color="crimson",
            fill=True,
        ).add_to(cluster)

    st_folium(m, use_container_width=True, height=700)
else:
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
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

st.download_button(
    "⬇️ Download filtered data (CSV)",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_incidents.csv",
    mime="text/csv"
)

st.info("👉 Change filters from the sidebar.")