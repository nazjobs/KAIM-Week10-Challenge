import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from src.data import load_data, get_observations, get_enriched_data, get_events

# Setup
os.makedirs("reports/figures", exist_ok=True)
sns.set_theme(style="whitegrid")


def plot_data_quality_summary(df):
    """Task 1: Explicit Data Quality & Coverage Analysis"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 1. Count by Record Type
    sns.countplot(data=df, x="record_type", ax=axes[0], palette="viridis")
    axes[0].set_title("Dataset Composition by Record Type")
    axes[0].set_ylabel("Count")

    # 2. Count by Confidence Level
    sns.countplot(
        data=df,
        x="confidence",
        ax=axes[1],
        palette="magma",
        order=["high", "medium", "low", "estimated"],
    )
    axes[1].set_title("Data Confidence Levels")

    plt.tight_layout()
    plt.savefig("reports/figures/data_quality_summary.png")
    print("Generated reports/figures/data_quality_summary.png")


def plot_event_timeline_dedicated(df):
    """Task 2: Dedicated Event Timeline Visualization"""
    events = get_events(df).copy()
    events = events.dropna(subset=["observation_date"])
    events = events.sort_values("observation_date")

    plt.figure(figsize=(12, 6))

    # Create a timeline where Y-axis is the category
    sns.scatterplot(
        data=events,
        x="observation_date",
        y="category",
        hue="category",
        s=200,
        marker="D",
        palette="deep",
        legend=False,
    )

    # Add vertical lines dropping to the x-axis
    for _, row in events.iterrows():
        plt.vlines(
            x=row["observation_date"],
            ymin=0,
            ymax=row["category"],
            color="grey",
            linestyle=":",
            alpha=0.5,
        )
        plt.text(
            row["observation_date"],
            row["category"],
            f" {row['indicator']}",
            verticalalignment="bottom",
            fontsize=9,
            rotation=20,
        )

    # Format X-axis
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    plt.title("Timeline of Financial Inclusion Events (2021-2025)")
    plt.grid(True, axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig("reports/figures/event_timeline.png")
    print("Generated reports/figures/event_timeline.png")


def plot_registered_vs_active(df):
    """Task 2: Registered vs Active Users (M-Pesa Case Study)"""
    # Filter specific records for M-Pesa
    mpesa_reg = df[df["indicator_code"] == "USG_MPESA_USERS"]
    mpesa_act = df[df["indicator_code"] == "USG_MPESA_ACTIVE"]

    if mpesa_reg.empty or mpesa_act.empty:
        return

    data = pd.concat([mpesa_reg, mpesa_act])

    plt.figure(figsize=(8, 6))
    ax = sns.barplot(data=data, x="indicator", y="value_numeric", palette="Blues_d")

    # Add values on top
    for i in ax.containers:
        ax.bar_label(i, fmt="%.0f", padding=3)

    plt.title('The "Activity Gap": Registered vs Active Users (M-Pesa 2025)')
    plt.ylabel("Users")
    plt.xlabel("")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig("reports/figures/registered_vs_active.png")
    print("Generated reports/figures/registered_vs_active.png")


def plot_access_trend(df):
    obs = get_observations(df, "ACCESS")
    acc_data = obs[obs["indicator_code"] == "ACC_OWNERSHIP"].sort_values(
        "observation_date"
    )
    acc_data = acc_data.dropna(subset=["observation_date"])

    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=acc_data,
        x="observation_date",
        y="value_numeric",
        marker="o",
        linewidth=2.5,
    )

    # Minimal event overlay (since we have a dedicated one now)
    plt.title("Account Ownership Trajectory (2014-2024)")
    plt.ylabel("Ownership (%)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("reports/figures/access_trend.png")
    print("Generated reports/figures/access_trend.png")


if __name__ == "__main__":
    df = load_data()
    df = get_enriched_data(df)

    plot_data_quality_summary(df)  # NEW
    plot_event_timeline_dedicated(df)  # NEW
    plot_registered_vs_active(df)  # NEW
    plot_access_trend(df)  # UPDATED
