"""Run the complete pipeline: data collection → building → forecasting → visualization."""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status."""
    logger.info("=== Step: {description} ===")
    logger.info(f"Command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        logger.error(
            f"✗ {description} failed with return code {result.returncode}",
            exc_info=True,
        )
        return False
    logger.info(f"✓ {description} completed successfully")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run complete Chronotopes of Culture pipeline"
    )
    parser.add_argument(
        "--skip-data-collection",
        action="store_true",
        help="Skip data collection step (use existing data)",
    )
    parser.add_argument(
        "--skip-forecasting",
        action="store_true",
        help="Skip forecasting step",
    )
    parser.add_argument(
        "--skip-visualization",
        action="store_true",
        help="Skip visualization step",
    )
    parser.add_argument(
        "--horizon",
        type=int,
        default=24,
        help="Forecast horizon in months (default: 24)",
    )
    return parser.parse_args()



def _step_collect_data(args, scripts_dir: Path) -> bool:
    """Step 1: Collect raw data (skippable)."""
    if args.skip_data_collection:
        logger.info("Skipping data collection (using existing data)")
        return True
    cmd = [sys.executable, str(scripts_dir / "collect_data.py"), "--datasets", "all"]
    ok = run_command(cmd, "Data Collection")
    if not ok:
        logger.error("Data collection failed — continuing with existing data.", exc_info=True)
    return ok


def _step_build_dataset(project_root: Path, scripts_dir: Path) -> bool:
    """Step 2: Build master dataset (required — exits on failure)."""
    cmd = [
        sys.executable, str(scripts_dir / "build_dataset.py"),
        "--catalog", str(project_root / "data_catalog.yaml"),
        "--output",  str(project_root / "data" / "master_dataset.parquet"),
    ]
    ok = run_command(cmd, "Build Master Dataset")
    if not ok:
        logger.error("Dataset building failed — cannot continue.", exc_info=True)
        sys.exit(1)
    return True


def _step_run_forecasts(args, project_root: Path, scripts_dir: Path) -> bool:
    """Step 3: Run forecasting models (skippable)."""
    if args.skip_forecasting:
        logger.info("Skipping forecasting")
        return True
    cmd = [
        sys.executable, str(scripts_dir / "run_forecasts.py"),
        "--input",   str(project_root / "data" / "master_dataset.parquet"),
        "--horizon", str(args.horizon),
        "--output",  str(project_root / "data" / "forecasts.parquet"),
    ]
    ok = run_command(cmd, "Run Forecasts")
    if not ok:
        logger.error("Forecasting failed — continuing.", exc_info=True)
    return ok


def _step_generate_visualizations(args, project_root: Path, scripts_dir: Path) -> bool:
    """Step 4: Generate visualizations (skippable)."""
    if args.skip_visualization:
        logger.info("Skipping visualization")
        return True
    forecast_file = project_root / "data" / "forecasts.parquet"
    cmd = [sys.executable, str(scripts_dir / "create_visualizations.py"),
           "--data-dir", str(project_root / "data")]
    if forecast_file.exists():
        cmd.extend(["--forecast-file", str(forecast_file)])
    ok = run_command(cmd, "Generate Visualizations")
    if not ok:
        logger.error("Visualization generation failed.", exc_info=True)
    return ok


def _step_narrative_brief(project_root: Path, scripts_dir: Path) -> bool:
    """Step 5: Generate narrative brief (skipped if no forecast file)."""
    forecast_file = project_root / "data" / "forecasts.parquet"
    if not forecast_file.exists():
        logger.info("Skipping narrative brief (no forecast file found)")
        return True
    cmd = [
        sys.executable, str(scripts_dir / "evaluate_narratives.py"),
        "--forecast-input", str(forecast_file),
        "--output", str(project_root / "reports" / "narrative_brief.md"),
    ]
    return run_command(cmd, "Generate Narrative Brief")


def main() -> None:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]
    scripts_dir  = project_root / "scripts"

    steps = [
        _step_collect_data(args, scripts_dir),
        _step_build_dataset(project_root, scripts_dir),
        _step_run_forecasts(args, project_root, scripts_dir),
        _step_generate_visualizations(args, project_root, scripts_dir),
        _step_narrative_brief(project_root, scripts_dir),
    ]
    completed = sum(steps)
    failed    = len(steps) - completed

    logger.info("=== Pipeline Summary ===")
    logger.info(f"Steps completed: {completed} / {len(steps)}")
    if failed == 0:
        logger.info("Pipeline completed successfully.")
    else:
        logger.error(f"Pipeline completed with {failed} failure(s).", exc_info=True)



if __name__ == "__main__":
    main()
