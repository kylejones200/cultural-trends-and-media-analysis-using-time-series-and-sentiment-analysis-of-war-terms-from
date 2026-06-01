"""Generated from Jupyter notebook: Notebook 01: Data Scraping & Ingestion

Magics and shell lines are commented out. Run with a normal Python interpreter."""

from pathlib import Path

import pandas as pd


def main():
    RAW_PATH = Path(
        "../../WIP/utilities/data/Hierarchical_Amtrak_Ridership.csv"
    ).resolve()
    INTERMEDIATE_DIR = Path("../data/intermediate").resolve()
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    amtrak_raw = pd.read_csv(RAW_PATH)
    amtrak_raw["ds"] = pd.to_datetime(amtrak_raw["year"], format="%Y")
    amtrak_agg = (
        amtrak_raw.groupby("ds", as_index=False)["Ridership"]
        .sum()
        .rename(columns={"Ridership": "y"})
    )
    amtrak_agg["unique_id"] = "amtrak_national"
    amtrak_agg = amtrak_agg[["unique_id", "ds", "y"]]
    output_path = INTERMEDIATE_DIR / "amtrak_ridership.csv"
    amtrak_agg.to_csv(output_path, index=False)
    amtrak_agg.head()


def main_alt() -> None:
    main()


if __name__ == "__main__":
    main()
