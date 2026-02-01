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
    sns.countplot(data=df, x="record_type", ax=axes[0], palette="viridis")
    axes[0].set_title("Dataset Composition by Record Type")
    axes[0].set_ylabel("Count")
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
    events = (
        get_events(df)
        .copy()
        .dropna(subset=["observation_date"])
        .sort_values("observation_date")
    )
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(
        data=events,
        x="observation_date",
        y="category",
        hue="category",
        s=300,
        marker="o",
        palette="deep",
        legend=False,
        ax=ax,
    )
    for _, row in events.iterrows():
        ax.vlines(
            x=row["observation_date"],
            ymin=0,
            ymax=row["category"],
            color="grey",
            linestyle=":",
            alpha=0.5,
        )
        ax.text(
            row["observation_date"],
            row["category"],
            f" {row['indicator']}",
            verticalalignment="bottom",
            fontsize=9,
            rotation=20,
        )
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.title("Timeline of Financial Inclusion Events (2021-2025)")
    plt.grid(True, axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig("reports/figures/event_timeline.png")
    print("Generated reports/figures/event_timeline.png")


def plot_registered_vs_active(df):
    """Task 2: Registered vs Active Users (M-Pesa Case Study)"""
    mpesa_reg = df[df["indicator_code"] == "USG_MPESA_USERS"].copy()
    mpesa_act = df[df["indicator_code"] == "USG_MPESA_ACTIVE"].copy()
    if mpesa_reg.empty or mpesa_act.empty:
        return
    mpesa_reg["Label"] = "Registered"
    mpesa_act["Label"] = "90-Day Active"
    data = pd.concat([mpesa_reg, mpesa_act])
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(data=data, x="Label", y="value_numeric", palette="Blues_d")
    for i in ax.containers:
        ax.bar_label(i, fmt="%.0f", padding=3)
    plt.title('The "Activity Gap": M-Pesa Users (2025)')
    plt.ylabel("Users (Millions)")
    plt.tight_layout()
    plt.savefig("reports/figures/registered_vs_active.png")
    print("Generated reports/figures/registered_vs_active.png")


def plot_infrastructure_vs_usage(df):
    """Task 2: Insight 3 - Infrastructure (4G) vs Usage (P2P)"""
    infra = df[df["indicator_code"] == "ACC_4G_COV"].sort_values("Year")
    usage = df[df["indicator_code"] == "USG_P2P_COUNT"].sort_values("Year")
    if infra.empty or usage.empty:
        return
    fig, ax1 = plt.subplots(figsize=(10, 6))
    color = "tab:red"
    ax1.set_xlabel("Year")
    ax1.set_ylabel("4G Population Coverage (%)", color=color)
    ax1.plot(
        infra["Year"], infra["value_numeric"], color=color, marker="o", linewidth=3
    )
    ax1.tick_params(axis="y", labelcolor=color)
    ax2 = ax1.twinx()
    color = "tab:blue"
    ax2.set_ylabel("P2P Transactions (Count)", color=color)
    ax2.plot(
        usage["Year"], usage["value_numeric"], color=color, marker="s", linestyle="--"
    )
    ax2.tick_params(axis="y", labelcolor=color)
    plt.title("Insight: Infrastructure Expansion Precedes Usage Spikes")
    fig.tight_layout()
    plt.savefig("reports/figures/infrastructure_vs_usage.png")
    print("Generated reports/figures/infrastructure_vs_usage.png")


def plot_affordability_shock(df):
    """Task 2: Insight 4 - Data Affordability & Shocks"""
    affordability = df[df["indicator_code"] == "AFF_DATA_INCOME"].sort_values(
        "observation_date"
    )
    if affordability.empty:
        return
    plt.figure(figsize=(10, 5))
    sns.lineplot(
        data=affordability,
        x="observation_date",
        y="value_numeric",
        marker="o",
        color="green",
    )
    fx_event = df[df["indicator_code"] == "EVT_FX_REFORM"]
    if not fx_event.empty:
        date = fx_event.iloc[0]["observation_date"]
        # --- THIS IS THE FIX ---
        if pd.notna(date):
            plt.axvline(
                x=date, color="orange", linestyle="--", label="FX Liberalization"
            )
            plt.text(
                date,
                affordability["value_numeric"].mean(),
                " FX Reform",
                color="orange",
                fontweight="bold",
            )
    plt.title("Data Affordability Index (Lower is Better)")
    plt.ylabel("Cost of 2GB Data (% of GNI)")
    plt.tight_layout()
    plt.savefig("reports/figures/affordability_trend.png")
    print("Generated reports/figures/affordability_trend.png")


if __name__ == "__main__":
    df = load_data()
    df = get_enriched_data(df)
    plot_data_quality_summary(df)
    plot_event_timeline_dedicated(df)
    plot_registered_vs_active(df)
    plot_infrastructure_vs_usage(df)
    plot_affordability_shock(df)
