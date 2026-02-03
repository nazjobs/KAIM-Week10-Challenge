import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide", page_title="Ethiopia Financial Inclusion Dashboard")


@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/inclusion_forecast.csv")
    df["date"] = pd.to_datetime(df["date"])
    impacts = pd.read_csv("data/processed/impact_matrix.csv")
    return df, impacts


try:
    df, impacts = load_data()
except:
    st.error("Run src/modeling.py first")
    st.stop()

st.title("🇪🇹 Ethiopia Financial Inclusion Forecasting (Global Findex)")
st.markdown(
    "Forecasting **Access** and **Usage** metrics against national targets (National Bank of Ethiopia)."
)

# --- SIDEBAR SCENARIOS ---
st.sidebar.header("Scenario Planning")
growth_rate = st.sidebar.slider("Projected Digital Adoption Rate (%)", -10, 20, 0)
target_val = st.sidebar.number_input(
    "2026 Inclusion Target (txn volume)", value=float(df["value"].max() * 1.2)
)

# Adjust forecast based on scenario
df["Scenario_Forecast"] = df["Forecast"] * (1 + growth_rate / 100)

# --- KPI ROW ---
col1, col2, col3 = st.columns(3)
curr_val = df["value"].iloc[-1]
proj_val = df["Scenario_Forecast"].iloc[-1]
gap = target_val - proj_val

col1.metric("Current Usage Metric", f"{curr_val:,.0f}")
col2.metric("Scenario Projection", f"{proj_val:,.0f}", delta=f"{growth_rate}%")
col3.metric("Gap to Target", f"{gap:,.0f}", delta_color="inverse")

# --- CHARTS ---
tab1, tab2 = st.tabs(["📈 Inclusion Forecast", "🔥 Impact Heatmap"])

with tab1:
    st.subheader("Financial Usage Forecast with Confidence Intervals")
    fig = go.Figure()

    # Historical
    fig.add_trace(
        go.Scatter(
            x=df["date"], y=df["value"], name="Actual Usage", line=dict(color="blue")
        )
    )

    # Forecast
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["Scenario_Forecast"],
            name="Forecast",
            line=dict(color="orange", dash="dash"),
        )
    )

    # Confidence Interval (Upper/Lower) - "Shaded Area"
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["Upper_Bound"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["Lower_Bound"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(255, 165, 0, 0.2)",
            name="95% Confidence Interval",
        )
    )

    # Target Line
    fig.add_hline(
        y=target_val,
        line_dash="dot",
        annotation_text="National Target",
        annotation_position="top right",
        line_color="green",
    )

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Event-Indicator Impact Matrix")
    # Heatmap of coefficients
    fig_heat = px.density_heatmap(
        impacts,
        x="Feature",
        y="Coefficient",
        z="Coefficient",
        color_continuous_scale="Viridis",
    )
    st.plotly_chart(fig_heat)
    st.markdown(
        "**Insight:** Holidays negatively impact digital usage, suggesting reliance on physical branches."
    )
