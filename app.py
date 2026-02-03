import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(page_title="KAIM Event Analytics", layout="wide")

# Title
st.title("📊 Financial Event Impact & Forecasting Dashboard")
st.markdown("Analysis of how holidays and events impact financial metrics.")


# Load Data (Cached)
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/processed/forecast_results.csv")
        impacts = pd.read_csv("data/processed/forecast_results_impacts.csv")
        return df, impacts
    except FileNotFoundError:
        return None, None


df, impacts = load_data()

if df is None:
    st.error("Data not found. Please run 'python src/modeling.py' first!")
    st.stop()

# Ensure date format
df["date"] = pd.to_datetime(df["date"])

# Sidebar Filters
st.sidebar.header("Filters")
min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Handle cases where user selects only one date
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# Filter Data
mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
filtered_df = df.loc[mask]

# --- KPI ROW ---
col1, col2, col3 = st.columns(3)

# Use 'target' column which represents the numeric value from your data
total_val = filtered_df["target"].sum()
avg_daily = filtered_df["target"].mean()
predicted_avg = (
    filtered_df["Forecast"].mean() if "Forecast" in filtered_df.columns else 0
)

col1.metric("Total Metric Value", f"{total_val:,.2f}")
col2.metric("Avg Daily Value (Actual)", f"{avg_daily:,.2f}")
col3.metric("Avg Daily Value (Forecast)", f"{predicted_avg:,.2f}")

st.divider()

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📈 Forecasting", "⚡ Event Impact", "📝 Recommendations"])

with tab1:
    st.subheader("Metric Forecast vs Actual")

    fig = go.Figure()
    # Actual Data
    fig.add_trace(
        go.Scatter(
            x=filtered_df["date"],
            y=filtered_df["target"],
            mode="lines+markers",
            name="Actual",
            line=dict(color="blue"),
        )
    )

    # Forecast Data (if available)
    if "Forecast" in filtered_df.columns:
        fig.add_trace(
            go.Scatter(
                x=filtered_df["date"],
                y=filtered_df["Forecast"],
                mode="lines",
                name="Predicted",
                line=dict(color="orange", dash="dash"),
            )
        )

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("How Events Impact Trends")
    st.markdown(
        "Positive values indicate an increase, negative values indicate a decrease."
    )

    if not impacts.empty:
        fig_bar = px.bar(
            impacts,
            x="Feature",
            y="Impact_Coefficient",
            color="Impact_Coefficient",
            color_continuous_scale="RdBu",
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.dataframe(impacts)
    else:
        st.info("No impact data available.")

with tab3:
    st.subheader("Strategic Recommendations")

    st.markdown("""
    Based on the analysis:
    
    1.  **Event Sensitivity:** If specific holidays show negative coefficients, plan maintenance or lower capacity during those times.
    2.  **Trend Awareness:** The forecast model captures seasonality. Use the 'Predicted' line to anticipate resource requirements 7 days out.
    3.  **Data Volume:** *Note: The current dataset is small. As more data is ingested, these trends will become statistically stronger.*
    """)
