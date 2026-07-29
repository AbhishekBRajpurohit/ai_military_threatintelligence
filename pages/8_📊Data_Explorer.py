import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Data Explorer", page_icon="📊", layout="wide")
st.title("📊 Data Explorer")
st.write("Filter, explore, and visualize the raw incident data.")

# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/globalterrorism.csv", encoding="latin-1", low_memory=False)

df = load_data()

# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------
st.sidebar.header("🔍 Filters")

year_min, year_max = int(df["iyear"].min()), int(df["iyear"].max())
year_range = st.sidebar.slider("Year Range", year_min, year_max, (year_min, year_max))

countries = st.sidebar.multiselect(
    "Country", sorted(df["country_txt"].dropna().unique().tolist())
)

attack_types = st.sidebar.multiselect(
    "Attack Type", sorted(df["attacktype1_txt"].dropna().unique().tolist())
)

# ---------------------------------------------------------
# Apply filters
# ---------------------------------------------------------
filtered = df[(df["iyear"] >= year_range[0]) & (df["iyear"] <= year_range[1])]

if countries:
    filtered = filtered[filtered["country_txt"].isin(countries)]
if attack_types:
    filtered = filtered[filtered["attacktype1_txt"].isin(attack_types)]

st.write(f"**{len(filtered):,} records** match your filters.")

# ---------------------------------------------------------
# Data table
# ---------------------------------------------------------
display_cols = [
    "iyear", "country_txt", "region_txt", "city", "attacktype1_txt",
    "targtype1_txt", "weaptype1_txt", "gname", "nkill", "nwound"
]
display_cols = [c for c in display_cols if c in filtered.columns]

st.dataframe(filtered[display_cols].head(500), use_container_width=True, height=350)

csv = filtered[display_cols].to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Filtered Data (CSV)", data=csv, file_name="filtered_data.csv", mime="text/csv")

st.markdown("---")

# ---------------------------------------------------------
# Charts
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    yearly = filtered.groupby("iyear").size().reset_index(name="Attacks")
    fig1 = px.bar(yearly, x="iyear", y="Attacks", title="Attacks per Year")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    top_targets = filtered["targtype1_txt"].value_counts().head(10).reset_index()
    top_targets.columns = ["Target Type", "Count"]
    fig2 = px.bar(top_targets, x="Count", y="Target Type", orientation="h",
                  title="Top Target Types")
    fig2.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------
# Map
# ---------------------------------------------------------
st.subheader("🗺️ Incident Map")

map_data = filtered.dropna(subset=["latitude", "longitude"]).head(1000)

if len(map_data) > 0:
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")

    for _, row in map_data.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=3,
            color="red",
            fill=True,
            fill_opacity=0.6,
            popup=f"{row.get('city', 'Unknown')}, {row.get('country_txt', '')} ({int(row['iyear'])})"
        ).add_to(m)

    st_folium(m, width=1200, height=500)
else:
    st.info("No geolocated records match your current filters.")
