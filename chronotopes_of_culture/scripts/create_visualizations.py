"""Generate publication-quality visualizations for the article."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import signalplot

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
# Set publication-quality style
plt.style.use("seaborn-v0_8-whitegrid")
signalplot.apply(font_family="serif")


def plot_time_series(
    df: pd.DataFrame, output_path: Path, title: str = None, plot: bool = False
) -> None:
    """Plot a single time series."""
    if not plot:
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["ds"], df["y"], linewidth=1.5, color="steelblue")
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Value", fontsize=12)
    if title:
        ax.set_title(title, fontsize=14, fontweight="bold")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_forecasts(
    historical: pd.DataFrame,
    forecasts: pd.DataFrame,
    output_path: Path,
    title: str = "Forecast Comparison",
) -> None:
    """Plot historical data with forecast overlays."""
    if not plot:
        return

    fig, ax = plt.subplots(figsize=(12, 6))
    # Plot historical
    ax.plot(
        historical["ds"],
        historical["y"],
        label="Historical",
        linewidth=2,
        color="steelblue",
    )
    # Plot forecasts by model
    model_colors = {
        "AutoARIMA": "coral",
        "SeasonalNaive": "forestgreen",
        "NHITS": "purple",
    }
    for model in forecasts["model"].unique():
        model_forecast = forecasts[forecasts["model"] == model].sort_values("ds")
        ax.plot(
            model_forecast["ds"],
            model_forecast["y"],
            label=f"{model} Forecast",
            linestyle="--",
            linewidth=1.5,
            color=model_colors.get(model, "gray"),
            alpha=0.8,
        )

    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Value", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend(loc="best", frameon=True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_cross_domain_comparison(
    commodities: pd.DataFrame,
    culture: pd.DataFrame,
    macro: pd.DataFrame,
    output_path: Path,
) -> None:
    """Create a multi-panel comparison across domains."""
    if not plot:
        return

    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    # Commodities
    for series_id in commodities["unique_id"].unique():
        subset = commodities[commodities["unique_id"] == series_id].sort_values("ds")
        axes[0].plot(
            subset["ds"],
            subset["y"],
            label=series_id.replace("_", " ").title(),
            linewidth=1.5,
        )
    axes[0].set_ylabel("Commodities", fontsize=12, fontweight="bold")
    axes[0].legend(loc="best")
    axes[0].set_title("Commodities", fontsize=13)
    # Culture
    for series_id in culture["unique_id"].unique():
        subset = culture[culture["unique_id"] == series_id].sort_values("ds")
        axes[1].plot(
            subset["ds"],
            subset["y"],
            label=series_id.replace("_", " ").title(),
            linewidth=1.5,
        )
    axes[1].set_ylabel("Culture", fontsize=12, fontweight="bold")
    axes[1].legend(loc="best")
    axes[1].set_title("Cultural Indicators", fontsize=13)
    # Macro
    for series_id in macro["unique_id"].unique():
        subset = macro[macro["unique_id"] == series_id].sort_values("ds")
        axes[2].plot(
            subset["ds"],
            subset["y"],
            label=series_id.replace("_", " ").title(),
            linewidth=1.5,
        )
    axes[2].set_ylabel("Macro", fontsize=12, fontweight="bold")
    axes[2].set_xlabel("Date", fontsize=12)
    axes[2].legend(loc="best")
    axes[2].set_title("Macroeconomic Indicators", fontsize=13)
    for ax in axes:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.xaxis.set_major_locator(mdates.YearLocator(2))

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_forecast_uncertainty(
    historical: pd.DataFrame,
    forecast_mean: pd.DataFrame,
    forecast_lower: pd.DataFrame = None,
    forecast_upper: pd.DataFrame = None,
    output_path: Path = None,
    title: str = "Forecast with Uncertainty",
) -> None:
    """Plot forecasts with confidence intervals."""
    if not plot:
        return

    fig, ax = plt.subplots(figsize=(12, 6))
    # Historical
    ax.plot(
        historical["ds"],
        historical["y"],
        label="Historical",
        linewidth=2,
        color="steelblue",
    )
    # Forecast mean
    ax.plot(
        forecast_mean["ds"],
        forecast_mean["y"],
        label="Forecast",
        linestyle="--",
        linewidth=2,
        color="coral",
    )
    # Uncertainty bands
    if forecast_lower is not None and forecast_upper is not None:
        ax.fill_between(
            forecast_mean["ds"],
            forecast_lower["y"],
            forecast_upper["y"],
            alpha=0.3,
            color="coral",
            label="95% Confidence Interval",
        )

    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Value", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend(loc="best")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.xticks(rotation=45)
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path)
    plt.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate visualizations for article")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
        help="Directory containing data files",
    )
    parser.add_argument(
        "--forecast-file",
        type=Path,
        default=None,
        help="Path to forecast output file (parquet or CSV)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "reports" / "figures",
        help="Directory to save figures",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    # Load master dataset
    master_path = args.data_dir / "master_dataset.parquet"
    if not master_path.exists():
        logger.info(f"Master dataset not found at {master_path}")
        logger.info("Run build_dataset.py first to create master dataset.")
        return

    df = pd.read_parquet(master_path)
    df["ds"] = pd.to_datetime(df["ds"])
    # Separate by domain
    commodities = df[df["unique_id"].isin(["gold_prices", "crude_oil"])]
    culture = df[df["unique_id"].isin(["film_releases", "book_sales"])]
    macro = df[df["unique_id"].isin(["inflation_cpi", "sentiment_index"])]
    df[df["unique_id"].str.contains("amtrak", case=False, na=False)]
    # Plot individual time series
    logger.info("Generating individual time series plots...")
    for series_id in df["unique_id"].unique():
        subset = df[df["unique_id"] == series_id].sort_values("ds")
        title = series_id.replace("_", " ").title()
        output_path = args.output_dir / f"{series_id}_timeseries.png"
        plot_time_series(subset, output_path, title=title)
        logger.info(f"  ✓ {series_id}")

    # Plot cross-domain comparison
    logger.info("Generating cross-domain comparison...")
    output_path = args.output_dir / "cross_domain_comparison.png"
    plot_cross_domain_comparison(commodities, culture, macro, output_path)
    logger.info("  ✓ Cross-domain comparison saved")
    # Plot forecasts if available
    if args.forecast_file and args.forecast_file.exists():
        logger.info("Generating forecast visualizations...")
        forecasts = (
            pd.read_parquet(args.forecast_file)
            if args.forecast_file.suffix == ".parquet"
            else pd.read_csv(args.forecast_file)
        )
        forecasts["ds"] = pd.to_datetime(forecasts["ds"])
        for series_id in forecasts["unique_id"].unique():
            series_historical = df[df["unique_id"] == series_id].sort_values("ds")
            series_forecasts = forecasts[
                forecasts["unique_id"] == series_id
            ].sort_values("ds")
            output_path = args.output_dir / f"{series_id}_forecasts.png"
            title = f"{series_id.replace('_', ' ').title()} Forecasts"
            plot_forecasts(
                series_historical, series_forecasts, output_path, title=title
            )
            logger.info(f"  ✓ {series_id} forecasts")

    logger.info(f"\n✓ All visualizations saved to {args.output_dir}")


if __name__ == "__main__":
    main()
