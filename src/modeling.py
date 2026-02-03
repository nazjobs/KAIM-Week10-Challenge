import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os


class InclusionModeler:
    def __init__(self, df):
        self.df = df.copy()
        self.model = LinearRegression()

    def preprocess(self):
        # Feature Engineering for Financial Inclusion Proxy
        self.df["day_of_week"] = self.df["date"].dt.dayofweek
        self.df["month"] = self.df["date"].dt.month
        self.df["lag_1"] = self.df["value"].shift(1).fillna(0)
        self.df["rolling_mean_3"] = self.df["value"].rolling(3).mean().fillna(0)
        return self.df

    def analyze_impact(self):
        # Task: Create Event-Indicator Matrix data
        data = self.preprocess()
        features = ["is_holiday", "day_of_week"]
        X = data[features]
        y = data["value"]

        self.model.fit(X, y)

        # heatmap data format
        impact_df = pd.DataFrame({"Feature": features, "Coefficient": self.model.coef_})
        return impact_df

    def forecast_with_confidence(self):
        data = self.preprocess()
        features = ["day_of_week", "month", "lag_1", "rolling_mean_3", "is_holiday"]
        X = data[features]
        y = data["value"]

        # Train
        self.model.fit(X, y)
        predictions = self.model.predict(X)

        # Calculate Confidence Intervals (95%)
        residuals = y - predictions
        std_dev = np.std(residuals)
        margin_of_error = 1.96 * std_dev

        data["Forecast"] = predictions
        data["Lower_Bound"] = predictions - margin_of_error
        data["Upper_Bound"] = predictions + margin_of_error

        return data


def run_pipeline():
    print("Loading Data...")
    # Load your specific file
    df = pd.read_csv("data/raw/ethiopia_fi_unified_data.csv")

    # MAPPING TO FINANCIAL INCLUSION CONTEXT
    # We treat 'value_numeric' as a proxy for "Digital Financial Service Usage"
    df.rename(
        columns={"observation_date": "date", "value_numeric": "value"}, inplace=True
    )
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "value"])

    # Aggregate to daily "Usage Score"
    daily = df.groupby("date")["value"].sum().reset_index()
    daily["is_holiday"] = daily["date"].dt.dayofweek.apply(
        lambda x: 1 if x >= 5 else 0
    )  # Mock holiday

    modeler = InclusionModeler(daily)

    # 1. Impacts
    impacts = modeler.analyze_impact()
    impacts.to_csv("data/processed/impact_matrix.csv", index=False)

    # 2. Forecasts with CI
    forecast = modeler.forecast_with_confidence()
    forecast.to_csv("data/processed/inclusion_forecast.csv", index=False)

    print("✅ Pipeline Complete: Generated forecasts with confidence intervals.")


if __name__ == "__main__":
    run_pipeline()
