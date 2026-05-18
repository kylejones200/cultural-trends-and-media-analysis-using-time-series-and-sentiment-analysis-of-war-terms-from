"""Generate all required datasets for the project."""

import logging
from datetime import datetime

import numpy as np
import pandas as pd

from scripts.collect_data import (
    fetch_sentiment,
    generate_synthetic_book_sales,
    generate_synthetic_film_releases,
)

logger = logging.getLogger(__name__)


def generate_amtrak_data():
    """Load and aggregate Amtrak data."""
    shared_path = (
        project_root.parent.parent / "data" / "amtrak_ridership_time_series_data.csv"
    )
    if shared_path.exists():
        df = pd.read_csv(shared_path)
        df["Year"] = pd.to_datetime(df["Year"])
        df_agg = df.groupby("Year")["Ridership"].sum().reset_index()
        df_agg["unique_id"] = "amtrak"
        df_agg.columns = ["ds", "y", "unique_id"]
        df_agg = df_agg[["unique_id", "ds", "y"]]
        df_agg = df_agg[df_agg["ds"] >= "2010-01-01"]
        return df_agg
    dates = pd.date_range(
        start="2010-01-01", end=datetime.now().strftime("%Y-%m-%d"), freq="MS"
    )
    np.random.seed(45)
    base = 3000000
    trend = np.linspace(0, 500000, len(dates))
    seasonal = 200000 * np.sin(2 * np.pi * (np.arange(len(dates)) - 6) / 12)
    noise = np.random.randn(len(dates)) * 100000
    covid_dip = np.where((dates >= "2020-03-01") & (dates < "2021-06-01"), -1500000, 0)
    ridership = base + trend + seasonal + noise + covid_dip
    ridership = np.maximum(ridership, 1000000)
    return pd.DataFrame({"unique_id": "amtrak", "ds": dates, "y": ridership})


def generate_cpi(start_date="2010-01-01", end_date=None):
    """Generate synthetic CPI inflation (YoY % change)."""
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    dates = pd.date_range(start=start_date, end=end_date, freq="MS")
    np.random.seed(44)
    base = 2.5
    trend = 0.5 * np.sin(2 * np.pi * np.arange(len(dates)) / 60)
    spikes = np.random.choice([0, 0, 0, 1, 2], len(dates)) * np.random.randn(len(dates))
    noise = np.random.randn(len(dates)) * 0.5
    inflation = base + trend + spikes + noise
    inflation = np.clip(inflation, -2, 8)
    return pd.DataFrame({"unique_id": "inflation_cpi", "ds": dates, "y": inflation})


def generate_gold_prices(start_date="2010-01-01", end_date=None):
    """Generate synthetic gold prices."""
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    dates = pd.date_range(start=start_date, end=end_date, freq="MS")
    np.random.seed(40)
    base = 1200
    trend = np.linspace(0, 800, len(dates))
    volatility = np.cumsum(np.random.randn(len(dates)) * 50)
    seasonal = 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
    prices = base + trend + volatility + seasonal
    prices = np.maximum(prices, 800)
    return pd.DataFrame({"unique_id": "gold_prices", "ds": dates, "y": prices})


def generate_oil_prices(start_date="2010-01-01", end_date=None):
    """Generate synthetic oil prices."""
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    dates = pd.date_range(start=start_date, end=end_date, freq="MS")
    np.random.seed(41)
    base = 60
    trend = np.linspace(0, 20, len(dates))
    cycles = 30 * np.sin(2 * np.pi * np.arange(len(dates)) / 36)
    volatility = np.cumsum(np.random.randn(len(dates)) * 5)
    prices = base + trend + cycles + volatility
    prices = np.maximum(prices, 20)
    return pd.DataFrame({"unique_id": "crude_oil", "ds": dates, "y": prices})


def gold_prices() -> None:
    "Generate all datasets."
    output_dir = project_root / "data" / "external"
    output_dir.mkdir(parents=True, exist_ok=True)
    intermediate_dir = project_root / "data" / "intermediate"
    intermediate_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Generating datasets...")
    logger.info("  Generating gold prices...")
    gold = generate_gold_prices()
    gold_path = output_dir / "commodities" / "gold_prices.csv"
    gold_path.parent.mkdir(parents=True, exist_ok=True)
    gold.to_csv(gold_path, index=False)
    logger.info(f"    ✓ Saved {len(gold)} records to {gold_path}")
    logger.info("  Generating oil prices...")
    oil = generate_oil_prices()
    oil_path = output_dir / "commodities" / "crude_oil.csv"
    oil_path.parent.mkdir(parents=True, exist_ok=True)
    oil.to_csv(oil_path, index=False)
    logger.info(f"    ✓ Saved {len(oil)} records to {oil_path}")
    logger.info("  Generating CPI inflation...")
    cpi = generate_cpi()
    cpi_path = output_dir / "macro" / "cpi.csv"
    cpi_path.parent.mkdir(parents=True, exist_ok=True)
    cpi.to_csv(cpi_path, index=False)
    logger.info(f"    ✓ Saved {len(cpi)} records to {cpi_path}")
    logger.info("  Generating sentiment index...")
    try:
        sentiment = fetch_sentiment()
    except Exception:
        dates = pd.date_range(
            start="2010-01-01", end=datetime.now().strftime("%Y-%m-%d"), freq="MS"
        )
        np.random.seed(42)
        base_sentiment = 100 + np.cumsum(np.random.randn(len(dates)) * 2)
        sentiment = pd.DataFrame(
            {"unique_id": "sentiment_index", "ds": dates, "y": base_sentiment}
        )

    sentiment_path = output_dir / "macro" / "sentiment_index.csv"
    sentiment_path.parent.mkdir(parents=True, exist_ok=True)
    sentiment.to_csv(sentiment_path, index=False)
    logger.info(f"    ✓ Saved {len(sentiment)} records to {sentiment_path}")
    logger.info("  Generating film releases...")
    film = generate_synthetic_film_releases()
    film_path = output_dir / "culture" / "film_releases.csv"
    film_path.parent.mkdir(parents=True, exist_ok=True)
    film.to_csv(film_path, index=False)
    logger.info(f"    ✓ Saved {len(film)} records to {film_path}")
    logger.info("  Generating book sales...")
    book = generate_synthetic_book_sales()
    book_path = output_dir / "culture" / "book_sales.csv"
    book_path.parent.mkdir(parents=True, exist_ok=True)
    book.to_csv(book_path, index=False)
    logger.info(f"    ✓ Saved {len(book)} records to {book_path}")
    logger.info("  Generating Amtrak data...")
    amtrak = generate_amtrak_data()
    amtrak_path = intermediate_dir / "amtrak_ridership.csv"
    amtrak.to_csv(amtrak_path, index=False)
    logger.info(f"    ✓ Saved {len(amtrak)} records to {amtrak_path}")
    logger.info("\n✓ All datasets generated successfully!")


def main() -> None:
    gold_prices()


if __name__ == "__main__":
    main()
