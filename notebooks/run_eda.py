import sys
import os

# Add parent directory to path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.data import load_data, get_observations, get_enriched_data, get_events

# Setup
os.makedirs("reports/figures", exist_ok=True)
sns.set_theme(style="whitegrid")


def plot_access_trend(df):
    """Task 2: Plot Account Ownership Trajectory"""
    obs = get_observations(df, "ACCESS")
    # Filter for the specific indicator 'ACC_OWNERSHIP'
    acc_data = obs[obs["indicator_code"] == "ACC_OWNERSHIP"].sort_values(
        "observation_date"
    )

    # Drop rows where observation_date is NaT
    acc_data = acc_data.dropna(subset=["observation_date"])

    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=acc_data,
        x="observation_date",
        y="value_numeric",
        marker="o",
        linewidth=2.5,
    )

    # Overlay events
    events = get_events(df)
    for _, event in events.iterrows():
        # CRITICAL FIX: Skip events with no valid date
        if pd.isna(event["observation_date"]):
            continue

        plt.axvline(x=event["observation_date"], color="red", linestyle="--", alpha=0.3)
        # Offset text slightly to avoid overlapping
        plt.text(
            event["observation_date"],
            20,
            f"  {event['indicator']}",
            rotation=90,
            fontsize=8,
            alpha=0.7,
        )

    plt.title("Ethiopia Account Ownership (2014-2024) with Key Events")
    plt.ylabel("Ownership (%)")
    plt.tight_layout()
    plt.savefig("reports/figures/access_trend.png")
    print("Generated reports/figures/access_trend.png")


def plot_mobile_vs_bank(df):
    """Task 2: Compare Traditional vs Mobile Money"""
    obs = get_observations(df, "ACCESS")
    mm_data = obs[obs["indicator_code"] == "ACC_MM_ACCOUNT"].copy()
    mm_data["Type"] = "Mobile Money"

    # Assuming ACC_OWNERSHIP is the total, we plot it for context
    total_data = obs[obs["indicator_code"] == "ACC_OWNERSHIP"].copy()
    total_data["Type"] = "Total Accounts"

    combined = pd.concat([mm_data, total_data])
    combined = combined.dropna(subset=["Year"])  # Ensure Year exists

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=combined, x="Year", y="value_numeric", hue="Type", palette="viridis"
    )
    plt.title("Mobile Money vs Total Account Ownership")
    plt.savefig("reports/figures/mobile_vs_total.png")
    print("Generated reports/figures/mobile_vs_total.png")


def plot_gender_gap(df):
    """Task 2: Gender Gap Analysis"""
    obs = get_observations(df, "GENDER")
    gap_data = obs[obs["indicator_code"] == "GEN_GAP_ACC"]
    gap_data = gap_data.dropna(subset=["Year"])

    plt.figure(figsize=(8, 5))
    sns.barplot(data=gap_data, x="Year", y="value_numeric", color="salmon")
    plt.title("Gender Gap in Account Ownership (Percentage Points)")
    plt.ylabel("Gap (Male % - Female %)")
    plt.savefig("reports/figures/gender_gap.png")
    print("Generated reports/figures/gender_gap.png")


if __name__ == "__main__":
    df = load_data()
    df = get_enriched_data(df)

    plot_access_trend(df)
    plot_mobile_vs_bank(df)
    plot_gender_gap(df)
