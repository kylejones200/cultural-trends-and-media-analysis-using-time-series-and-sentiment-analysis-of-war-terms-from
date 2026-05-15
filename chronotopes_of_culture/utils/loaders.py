"""Utility functions for loading catalogued datasets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def load_source(name: str, meta: dict[str, Any]) -> pd.DataFrame:
    """Load a dataset using metadata from ``data_catalog.yaml``.

    Parameters
    ----------
    name:
        Identifier of the dataset.
    meta:
        Metadata dictionary containing at least ``source``, ``time_col``, ``value_col``.

    Returns
    -------
    pd.DataFrame
        A dataframe standardized to columns ``['unique_id', 'ds', 'y']``.
    """

    source_path = Path(meta["source"]).expanduser()
    if not source_path.is_absolute():
        source_path = Path(__file__).resolve().parents[1] / source_path

    if not source_path.exists():
        raise FileNotFoundError(f"Dataset '{name}' not found at {source_path}")

    df = pd.read_csv(source_path)

    time_col = meta.get("time_col", "date")
    value_col = meta.get("value_col", "value")

    df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
    df = df.dropna(subset=[time_col, value_col])

    df = df.rename(columns={time_col: "ds", value_col: "y"})
    df["unique_id"] = meta.get("unique_id", meta.get("tags", [name])[0])

    ordered_cols = [
        "unique_id",
        "ds",
        "y",
        *[c for c in df.columns if c not in {"unique_id", "ds", "y"}],
    ]
    return df[ordered_cols]
