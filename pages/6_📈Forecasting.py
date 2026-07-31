import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet
from utils.data_loader import load_data

st.set_page_config(page_title="Forecasting", page_icon="📈", layout="wide")
st.title("📈 Attack Trend Forecasting")
st.write("Forecast future incident trends using historical data (Prophet time-series model).")

df = load_data()

col1, col2 = st.columns(2)
with col1:
    countries = ["All"] + sorted(df["country_txt"].dropna().unique().tolist())
    selected_country = st.selectbox("🌍 Filter by Country", countries)

with col2:
    periods = st.slider("Forecast horizon (years)", min_value=1, max_value=10, value=5)

if selected_country != "All":
    filtered = df[df["country_txt"] == selected_country]
else:
    filtered = df

yearly_counts = (
    filtered.groupby("iyear", observed=True)
    .size()
    .reset_index(name="attacks")
    .rename(columns={"iyear": "ds", "attacks": "y"})
)

MIN_POINTS = 8


@st.cache_resource(show_spinner="Training forecasting model...")
def fit_prophet(year_count_pairs, periods):
    """year_count_pairs must be a hashable tuple for caching to work."""
    yc = pd.DataFrame(year_count_pairs, columns=["ds", "y"])
    yc["ds"] = pd.to_datetime(yc["ds"], format="%Y")
    model = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
    model.fit(yc)
    future = model.make_future_dataframe(periods=periods, freq="YE")
    forecast = model.predict(future)
    return forecast, yc


if len(yearly_counts) < MIN_POINTS:
    st.warning(
        f"Only {len(yearly_counts)} yearly data points for this filter. "
        f"Forecasts need at least {MIN_POINTS} points to be reasonably stable — "
        "try 'All' countries or a broader time range."
    )
else:
    pairs = tuple(zip(yearly_counts["ds"].tolist(), yearly_counts["y"].tolist()))
    forecast, yearly_counts_ts = fit_prophet(pairs, periods)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=yearly_counts_ts["ds"], y=yearly_counts_ts["y"],
        mode="markers+lines", name="Historical Attacks", line=dict(color="#3498db")
    ))

    fig.add_trace(go.Scatter(
        x=forecast["ds"], y=forecast["yhat"],
        mode="lines", name="Forecast", line=dict(color="#e74c3c", dash="dash")
    ))

    fig.add_trace(go.Scatter(
        x=pd.concat([forecast["ds"], forecast["ds"][::-1]]),
        y=pd.concat([forecast["yhat_upper"], forecast["yhat_lower"][::-1]]),
        fill="toself", fillcolor="rgba(231,76,60,0.15)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Confidence Interval", showlegend=True
    ))

    fig.update_layout(
        title=f"Attack Frequency Forecast — {selected_country}",
        xaxis_title="Year", yaxis_title="Number of Attacks",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Forecast Data")
    display_cols = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods)
    display_cols.columns = ["Year", "Predicted Attacks", "Lower Bound", "Upper Bound"]
    display_cols["Year"] = display_cols["Year"].dt.year
    st.dataframe(display_cols.round(1), use_container_width=True)