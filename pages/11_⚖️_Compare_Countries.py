import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import load_data
from utils.auth_ui import require_login

require_login()

st.set_page_config(page_title="Compare Countries", page_icon="⚖️", layout="wide")
st.title("⚖️ Compare Countries")

df = load_data()

all_countries = sorted(df["country_txt"].dropna().unique().tolist())

selected = st.multiselect(
    "Select 2 or more countries to compare",
    all_countries,
    default=all_countries[:2] if len(all_countries) >= 2 else all_countries
)

if len(selected) < 2:
    st.info("Select at least 2 countries to see a comparison.")
    st.stop()

compare_df = df[df["country_txt"].isin(selected)]

st.subheader("📊 Summary Comparison")

summary_rows = []
for country in selected:
    cdf = compare_df[compare_df["country_txt"] == country]
    summary_rows.append({
        "Country": country,
        "Incidents": len(cdf),
        "Fatalities": int(cdf["nkill"].sum()),
        "Injured": int(cdf["nwound"].sum()),
        "Years Active": f"{int(cdf['iyear'].min())}–{int(cdf['iyear'].max())}",
        "Most Common Attack": cdf["attacktype1_txt"].value_counts().idxmax() if len(cdf) else "N/A",
    })

st.dataframe(summary_rows, use_container_width=True)

st.divider()

st.subheader("📈 Attacks Over Time")

fig = go.Figure()
for country in selected:
    cdf = compare_df[compare_df["country_txt"] == country]
    yearly = cdf.groupby("iyear", observed=True).size().reset_index(name="Attacks")
    fig.add_trace(go.Scatter(
        x=yearly["iyear"], y=yearly["Attacks"],
        mode="lines+markers", name=country
    ))

fig.update_layout(xaxis_title="Year", yaxis_title="Number of Attacks", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("🔫 Weapon Type Usage")

weapon_counts = (
    compare_df.groupby(["country_txt", "weaptype1_txt"], observed=True)
    .size()
    .reset_index(name="Count")
)

fig2 = px.bar(
    weapon_counts, x="weaptype1_txt", y="Count", color="country_txt",
    barmode="group", title="Weapon Type by Country"
)
fig2.update_layout(xaxis_title="Weapon Type", yaxis_title="Attacks")
st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("🎯 Target Type Usage")

target_counts = (
    compare_df.groupby(["country_txt", "targtype1_txt"], observed=True)
    .size()
    .reset_index(name="Count")
)

fig3 = px.bar(
    target_counts, x="targtype1_txt", y="Count", color="country_txt",
    barmode="group", title="Target Type by Country"
)
fig3.update_layout(xaxis_title="Target Type", yaxis_title="Attacks")
st.plotly_chart(fig3, use_container_width=True)