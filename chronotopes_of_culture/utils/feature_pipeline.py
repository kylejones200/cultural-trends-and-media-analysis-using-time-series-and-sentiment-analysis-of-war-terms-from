"""Feature engineering helpers for cultural futures forecasting."""

from __future__ import annotations

import pandas as pd


def harmonize_timeseries(df: pd.DataFrame) -> pd.DataFrame:
    """Apply basic cleaning/normalization to combined datasets."""
    df = df.copy()
    df["ds"] = pd.to_datetime(df["ds"], errors="coerce")
    df = df.dropna(subset=["ds", "y"]).sort_values("ds")
    df["y"] = df["y"].astype(float)
    return df


def prepare_forecast_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure dataframe is ready for StatsForecast / NeuralForecast APIs."""
    required = {"unique_id", "ds", "y"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataframe missing required columns: {missing}")
    result = df.copy()
    result = result.sort_values(["unique_id", "ds"])
    return result
