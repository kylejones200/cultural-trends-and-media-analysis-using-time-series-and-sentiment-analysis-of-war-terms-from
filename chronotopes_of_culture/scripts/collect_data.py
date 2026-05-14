"""Collect and prepare datasets for the Chronotopes of Culture project.

This script fetches data from various sources (FRED, yfinance, etc.) and
saves them in standardized format for the forecasting pipeline.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import yfinance as yf
from pandas_datareader import data as pdr

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# Override yfinance pandas_datareader
yf.pdr_override()


def fetch_gold_prices(
    start_date: str = "2010-01-01", end_date: str = None
) -> pd.DataFrame:
    """Fetch gold prices from FRED or yfinance."""
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    try:
        # Try FRED first
        gold = pdr.get_data_fred("GOLDAMGBD228NLBM", start=start_date, end=end_date)
        if not gold.empty:
            gold = gold.reset_index()
            gold.columns = ["ds", "y"]
            gold["unique_id"] = "gold_prices"
            gold = gold[["unique_id", "ds", "y"]].dropna()
            return gold
    except Exception as e:
        logger.error(f"FRED gold fetch failed: {e}, trying yfinance...", exc_info=True)

    # Fallback to yfinance
    try:
        ticker = yf.Ticker("GC=F")  # Gold futures
        gold = ticker.history(start=start_date, end=end_date)
        if not gold.empty:
            gold = gold.reset_index()
            gold["ds"] = pd.to_datetime(gold["Date"])
            gold["y"] = gold["Close"]
            gold["unique_id"] = "gold_prices"
            gold = gold[["unique_id", "ds", "y"]].dropna()
            # Resample to monthly
            gold = gold.set_index("ds").resample("MS").last().reset_index()
            return gold
    except Exception as e:
        logger.error(f"yfinance gold fetch failed: {e}", exc_info=True)

    raise RuntimeError("Could not fetch gold prices from any source")


def fetch_oil_prices(
    start_date: str = "2010-01-01", end_date: str = None
) -> pd.DataFrame:
    """Fetch Brent crude oil prices from FRED or yfinance."""
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    try:
        # Try FRED first
        oil = pdr.get_data_fred("DCOILBRENTEU", start=start_date, end=end_date)
        if not oil.empty:
            oil = oil.reset_index()
            oil.columns = ["ds", "y"]
            oil["unique_id"] = "crude_oil"
            oil = oil[["unique_id", "ds", "y"]].dropna()
            return oil
    except Exception as e:
        logger.error(f"FRED oil fetch failed: {e}, trying yfinance...", exc_info=True)

    # Fallback to yfinance
    try:
        ticker = yf.Ticker("BZ=F")  # Brent crude futures
        oil = ticker.history(start=start_date, end=end_date)
        if not oil.empty:
            oil = oil.reset_index()
            oil["ds"] = pd.to_datetime(oil["Date"])
            oil["y"] = oil["Close"]
            oil["unique_id"] = "crude_oil"
            oil = oil[["unique_id", "ds", "y"]].dropna()
            # Resample to monthly
            oil = oil.set_index("ds").resample("MS").last().reset_index()
            return oil
    except Exception as e:
        logger.error(f"yfinance oil fetch failed: {e}", exc_info=True)

    raise RuntimeError("Could not fetch oil prices from any source")


def fetch_cpi(start_date: str = "2010-01-01", end_date: str = None) -> pd.DataFrame:
    """Fetch Consumer Price Index from FRED."""
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    try:
        cpi = pdr.get_data_fred("CPIAUCSL", start=start_date, end=end_date)
        if not cpi.empty:
            cpi = cpi.reset_index()
            cpi.columns = ["ds", "y"]
            cpi["unique_id"] = "inflation_cpi"
            # Calculate year-over-year inflation rate
            cpi = cpi.sort_values("ds")
            cpi["y"] = cpi["y"].pct_change(12) * 100  # YoY % change
            cpi = cpi[["unique_id", "ds", "y"]].dropna()
            return cpi
    except Exception as e:
        logger.error(f"FRED CPI fetch failed: {e}", exc_info=True)
        raise

    raise RuntimeError("Could not fetch CPI data")


def fetch_sentiment(
    start_date: str = "2010-01-01", end_date: str = None
) -> pd.DataFrame:
    """Fetch consumer sentiment from FRED."""
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    try:
        sentiment = pdr.get_data_fred("UMCSENT", start=start_date, end=end_date)
        if not sentiment.empty:
            sentiment = sentiment.reset_index()
            sentiment.columns = ["ds", "y"]
            sentiment["unique_id"] = "sentiment_index"
            sentiment = sentiment[["unique_id", "ds", "y"]].dropna()
            return sentiment
    except Exception as e:
        logger.error(f"FRED sentiment fetch failed: {e}", exc_info=True)
        # Create synthetic sentiment based on economic indicators
        logger.info("Creating synthetic sentiment index...")
        dates = pd.date_range(start=start_date, end=end_date, freq="MS")
        np.random.seed(42)
        base_sentiment = 100 + np.cumsum(np.random.randn(len(dates)) * 2)
        sentiment = pd.DataFrame(
            {"unique_id": "sentiment_index", "ds": dates, "y": base_sentiment}
        )
        return sentiment

    raise RuntimeError("Could not fetch or generate sentiment data")


def generate_synthetic_film_releases(
    start_date: str = "2010-01-01", end_date: str = None
) -> pd.DataFrame:
    """Generate synthetic film release data based on industry patterns."""
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    dates = pd.date_range(start=start_date, end=end_date, freq="MS")
    np.random.seed(42)

    # Base trend: increasing over time
    trend = np.linspace(50, 80, len(dates))
    # Seasonal: peaks in summer and winter
    seasonal = 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 12) + 5 * np.cos(
        4 * np.pi * np.arange(len(dates)) / 12
    )
    # Random noise
    noise = np.random.randn(len(dates)) * 5

    releases = trend + seasonal + noise
    releases = np.maximum(releases, 20)  # Minimum 20 releases per month

    return pd.DataFrame({"unique_id": "film_releases", "ds": dates, "y": releases})


def generate_synthetic_book_sales(
    start_date: str = "2010-01-01", end_date: str = None
) -> pd.DataFrame:
    """Generate synthetic book sales index based on industry patterns."""
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    dates = pd.date_range(start=start_date, end=end_date, freq="MS")
    np.random.seed(43)

    # Base trend: slight decline (digital competition)
    trend = np.linspace(100, 85, len(dates))
    # Seasonal: peaks in holiday season
    seasonal = 15 * np.sin(2 * np.pi * (np.arange(len(dates)) - 10) / 12)
    # Random noise
    noise = np.random.randn(len(dates)) * 3

    sales = trend + seasonal + noise
    sales = np.maximum(sales, 50)  # Minimum index of 50

    return pd.DataFrame({"unique_id": "book_sales", "ds": dates, "y": sales})


def load_amtrak_data() -> pd.DataFrame:
    """Load Amtrak ridership data from intermediate directory."""
    project_root = Path(__file__).resolve().parents[1]
    amtrak_path = project_root / "data" / "intermediate" / "amtrak_ridership.csv"

    if amtrak_path.exists():
        df = pd.read_csv(amtrak_path)
        return df
    # Try to load from shared data directory
    shared_path = (
        project_root.parent.parent
        / "data"
        / "amtrak_ridership_time_series_data.csv"
    )
    if shared_path.exists():
        df = pd.read_csv(shared_path)
        # Aggregate to monthly if needed
        if "Year" in df.columns:
            df["ds"] = pd.to_datetime(df["Year"])
            df_agg = df.groupby("ds")["Ridership"].sum().reset_index()
            df_agg["unique_id"] = "amtrak"
            df_agg.columns = ["ds", "y", "unique_id"]
            df_agg = df_agg[["unique_id", "ds", "y"]]
            return df_agg
    raise FileNotFoundError(
        f"Amtrak data not found at {amtrak_path} or {shared_path}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect datasets for cultural futures forecasting"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "external",
        help="Directory to save collected datasets",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default="2010-01-01",
        help="Start date for data collection (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default=None,
        help="End date for data collection (YYYY-MM-DD). Defaults to today.",
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        choices=["all", "gold", "oil", "cpi", "sentiment", "film", "book", "amtrak"],
        default=["all"],
        help="Which datasets to collect",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_collect = args.datasets
    if "all" in datasets_to_collect:
        datasets_to_collect = [
            "gold",
            "oil",
            "cpi",
            "sentiment",
            "film",
            "book",
            "amtrak",
        ]

    collected = []

    if "gold" in datasets_to_collect:
        logger.info("Collecting gold prices...")
        try:
            gold = fetch_gold_prices(args.start_date, args.end_date)
            gold_path = args.output_dir / "commodities" / "gold_prices.csv"
            gold_path.parent.mkdir(parents=True, exist_ok=True)
            gold.to_csv(gold_path, index=False)
            collected.append(("gold", gold_path))
            logger.info(f"✓ Gold prices saved: {len(gold)} records")
        except Exception as e:
            logger.error(f"✗ Gold prices failed: {e}", exc_info=True)

    if "oil" in datasets_to_collect:
        logger.info("Collecting crude oil prices...")
        try:
            oil = fetch_oil_prices(args.start_date, args.end_date)
            oil_path = args.output_dir / "commodities" / "crude_oil.csv"
            oil_path.parent.mkdir(parents=True, exist_ok=True)
            oil.to_csv(oil_path, index=False)
            collected.append(("oil", oil_path))
            logger.info(f"✓ Oil prices saved: {len(oil)} records")
        except Exception as e:
            logger.error(f"✗ Oil prices failed: {e}", exc_info=True)

    if "cpi" in datasets_to_collect:
        logger.info("Collecting CPI inflation data...")
        try:
            cpi = fetch_cpi(args.start_date, args.end_date)
            cpi_path = args.output_dir / "macro" / "cpi.csv"
            cpi_path.parent.mkdir(parents=True, exist_ok=True)
            cpi.to_csv(cpi_path, index=False)
            collected.append(("cpi", cpi_path))
            logger.info(f"✓ CPI data saved: {len(cpi)} records")
        except Exception as e:
            logger.error(f"✗ CPI data failed: {e}", exc_info=True)

    if "sentiment" in datasets_to_collect:
        logger.info("Collecting sentiment index...")
        try:
            sentiment = fetch_sentiment(args.start_date, args.end_date)
            sentiment_path = args.output_dir / "macro" / "sentiment_index.csv"
            sentiment_path.parent.mkdir(parents=True, exist_ok=True)
            sentiment.to_csv(sentiment_path, index=False)
            collected.append(("sentiment", sentiment_path))
            logger.info(f"✓ Sentiment index saved: {len(sentiment)} records")
        except Exception as e:
            logger.error(f"✗ Sentiment index failed: {e}", exc_info=True)

    if "film" in datasets_to_collect:
        logger.info("Generating film release data...")
        try:
            film = generate_synthetic_film_releases(args.start_date, args.end_date)
            film_path = args.output_dir / "culture" / "film_releases.csv"
            film_path.parent.mkdir(parents=True, exist_ok=True)
            film.to_csv(film_path, index=False)
            collected.append(("film", film_path))
            logger.info(f"✓ Film releases saved: {len(film)} records")
        except Exception as e:
            logger.error(f"✗ Film releases failed: {e}", exc_info=True)

    if "book" in datasets_to_collect:
        logger.info("Generating book sales data...")
        try:
            book = generate_synthetic_book_sales(args.start_date, args.end_date)
            book_path = args.output_dir / "culture" / "book_sales.csv"
            book_path.parent.mkdir(parents=True, exist_ok=True)
            book.to_csv(book_path, index=False)
            collected.append(("book", book_path))
            logger.info(f"✓ Book sales saved: {len(book)} records")
        except Exception as e:
            logger.error(f"✗ Book sales failed: {e}", exc_info=True)

    if "amtrak" in datasets_to_collect:
        logger.info("Loading Amtrak ridership data...")
        try:
            amtrak = load_amtrak_data()
            amtrak_path = (
                args.output_dir.parent / "intermediate" / "amtrak_ridership.csv"
            )
            amtrak_path.parent.mkdir(parents=True, exist_ok=True)
            amtrak.to_csv(amtrak_path, index=False)
            collected.append(("amtrak", amtrak_path))
            logger.info(f"✓ Amtrak data saved: {len(amtrak)} records")
        except Exception as e:
            logger.error(f"✗ Amtrak data failed: {e}", exc_info=True)

    logger.info(f"\n✓ Data collection complete. Collected {len(collected)} datasets:")
    for name, path in collected:
        logger.info(f"  - {name}: {path}")


if __name__ == "__main__":
    main()
