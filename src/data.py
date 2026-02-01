import pandas as pd
from pathlib import Path


def load_data(path: str = "data/raw/ethiopia_fi_unified_data.csv") -> pd.DataFrame:
    """
    Loads the unified financial inclusion dataset.
    Ensures dates are parsed and numeric columns are correct.
    """
    # Use path relative to the script execution or absolute
    base_path = Path(__file__).parent.parent
    full_path = base_path / path

    if not full_path.exists():
        # Fallback for running from root
        full_path = path

    df = pd.read_csv(full_path)

    # Parse Dates
    df["observation_date"] = pd.to_datetime(df["observation_date"], errors="coerce")

    # Ensure numeric columns
    numeric_cols = ["value_numeric", "impact_estimate", "lag_months"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def get_observations(df: pd.DataFrame, pillar: str = None) -> pd.DataFrame:
    """Filter for observations, optionally by pillar."""
    mask = df["record_type"] == "observation"
    if pillar:
        mask &= df["pillar"] == pillar
    return df[mask].copy()


def get_events(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for events."""
    return df[df["record_type"] == "event"].copy()


def get_enriched_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Task 1 Enrichment:
    Create a clean Year column from observation_date for plotting.
    """
    df["Year"] = df["observation_date"].dt.year
    return df
