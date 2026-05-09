"""Run multi-model forecasts for the Chronotopes of Culture project."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, SeasonalNaive
from neuralforecast import NeuralForecast
from neuralforecast.models import NHITS

from utils.feature_pipeline import prepare_forecast_frame


import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute forecast pipelines for the cultural futures project"
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "master_dataset.parquet",
        help="Path to harmonized dataset",
    )
    parser.add_argument(
        "--horizon", type=int, default=12, help="Forecast horizon (in time periods)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "reports"
        / "forecast_outputs.parquet",
        help="Where to store consolidated forecasts",
    )
    return parser.parse_args()


def run_statsforecast(df: pd.DataFrame, horizon: int) -> pd.DataFrame:
    models = [AutoARIMA(), SeasonalNaive(season_length=12)]
    sf = StatsForecast(models=models, freq="MS", n_jobs=-1)
    forecasts = sf.forecast(df=df, h=horizon)
    forecasts["model_family"] = "StatsForecast"
    return forecasts


def run_neuralforecast(df: pd.DataFrame, horizon: int) -> pd.DataFrame:
    nf = NeuralForecast(models=[NHITS(h=horizon, input_size=24)], freq="MS")
    nf.fit(df)
    forecasts = nf.predict().reset_index()
    forecasts["model_family"] = "NeuralForecast"
    return forecasts


def main() -> None:
    args = parse_args()
    ds = pd.read_parquet(args.input)
    base = prepare_forecast_frame(ds)

    stats_results = run_statsforecast(base, args.horizon)
    neural_results = run_neuralforecast(base, args.horizon)

    combined = pd.concat([stats_results, neural_results], ignore_index=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    combined.to_parquet(args.output)
    logger.info(f"✓ Forecasts written -> {args.output}")


if __name__ == "__main__":
    main()
