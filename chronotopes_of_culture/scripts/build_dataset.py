"""Builds the unified cultural futures dataset.

This script reads sources declared in ``data_catalog.yaml`` and writes
standardized parquet/csv files for forecasting pipelines.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd
import yaml
from utils.feature_pipeline import harmonize_timeseries
from utils.loaders import load_source

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build consolidated dataset for cultural futures forecasting"
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data_catalog.yaml",
        help="Path to data catalog YAML file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "master_dataset.parquet",
        help="Output path for harmonized dataset",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with open(args.catalog, encoding="utf-8") as fh:
        catalog = yaml.safe_load(fh)

    frames: list[pd.DataFrame] = []
    for domain, entries in catalog.items():
        if domain == "notes":
            continue
        for name, meta in entries.items():
            df = load_source(name, meta)
            df["domain"] = domain
            df["series_name"] = name
            frames.append(df)

    if not frames:
        raise RuntimeError(
            "No datasets were loaded. Update data_catalog.yaml with valid sources."
        )

    combined = pd.concat(frames, ignore_index=True)
    harmonized = harmonize_timeseries(combined)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    harmonized.to_parquet(args.output)
    logger.info(f"✓ Master dataset written -> {args.output}")


if __name__ == "__main__":
    main()
