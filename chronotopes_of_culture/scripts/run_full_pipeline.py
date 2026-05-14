"""Run the complete pipeline: data collection → building → forecasting → visualization."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status."""
    logger.info("=== Step: {description} ===")
    logger.info(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        logger.error(f"✗ {description} failed with return code {result.returncode}", exc_info=True)
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


def main() -> None:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]
    scripts_dir = project_root / "scripts"

    steps_completed = 0
    steps_failed = 0

    # Step 1: Data Collection
    if not args.skip_data_collection:
        cmd = [
            sys.executable,
            str(scripts_dir / "collect_data.py"),
            "--datasets",
            "all",
        ]
        if run_command(cmd, "Data Collection"):
            steps_completed += 1
        else:
            steps_failed += 1
            logger.error("Warning: Data collection failed, but continuing...", exc_info=True)
    else:
        logger.info("Skipping data collection (using existing data)")
        steps_completed += 1

    # Step 2: Build Dataset
    cmd = [
        sys.executable,
        str(scripts_dir / "build_dataset.py"),
        "--catalog",
        str(project_root / "data_catalog.yaml"),
        "--output",
        str(project_root / "data" / "master_dataset.parquet"),
    ]
    if run_command(cmd, "Build Master Dataset"):
        steps_completed += 1
    else:
        steps_failed += 1
        logger.error("Error: Dataset building failed. Cannot continue.", exc_info=True)
        sys.exit(1)

    # Step 3: Run Forecasts
    if not args.skip_forecasting:
        forecast_output = project_root / "data" / "forecasts.parquet"
        cmd = [
            sys.executable,
            str(scripts_dir / "run_forecasts.py"),
            "--input",
            str(project_root / "data" / "master_dataset.parquet"),
            "--horizon",
            str(args.horizon),
            "--output",
            str(forecast_output),
        ]
        if run_command(cmd, "Run Forecasts"):
            steps_completed += 1
        else:
            steps_failed += 1
            logger.error("Warning: Forecasting failed, but continuing...", exc_info=True)
    else:
        logger.info("Skipping forecasting")
        steps_completed += 1

    # Step 4: Generate Visualizations
    if not args.skip_visualization:
        forecast_file = project_root / "data" / "forecasts.parquet"
        if not forecast_file.exists():
            forecast_file = None

        cmd = [
            sys.executable,
            str(scripts_dir / "create_visualizations.py"),
            "--data-dir",
            str(project_root / "data"),
        ]
        if forecast_file:
            cmd.extend(["--forecast-file", str(forecast_file)])

        if run_command(cmd, "Generate Visualizations"):
            steps_completed += 1
        else:
            steps_failed += 1
            logger.error("Warning: Visualization generation failed", exc_info=True)
    else:
        logger.info("Skipping visualization")
        steps_completed += 1

    # Step 5: Generate Narrative Brief
    forecast_file = project_root / "data" / "forecasts.parquet"
    if forecast_file.exists():
        cmd = [
            sys.executable,
            str(scripts_dir / "evaluate_narratives.py"),
            "--forecast-input",
            str(forecast_file),
            "--output",
            str(project_root / "reports" / "narrative_brief.md"),
        ]
        if run_command(cmd, "Generate Narrative Brief"):
            steps_completed += 1
        else:
            steps_failed += 1
    else:
        logger.info("Skipping narrative brief (no forecast file found)")

    # Summary
    logger.info("=== Pipeline Summary ===")
    logger.info(f"Steps completed: {steps_completed}")
    logger.error(f"Steps failed: {steps_failed}", exc_info=True)

    if steps_failed == 0:
        logger.info("\n✓ Pipeline completed successfully!")
    else:
        logger.error(f"\n⚠ Pipeline completed with {steps_failed} warning(s, exc_info=True)")


if __name__ == "__main__":
    main()
