# How to Execute the Pipeline

Since the shell environment has issues, here's how to manually complete the remaining TODOs:

## Step 1: Generate Data Files

Run this Python script to create all data files:

```bash
cd /Users/kylejonespatricia/time_series/WIP/chronotopes_of_culture
python3 scripts/generate_all_data.py
```

Or run it interactively in Python:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('scripts').resolve()))
from generate_all_data import main
main()
```

## Step 2: Build Master Dataset

```bash
python3 scripts/build_dataset.py
```

## Step 3: Run Forecasts

```bash
python3 scripts/run_forecasts.py --input data/master_dataset.parquet --horizon 24 --output data/forecasts.parquet
```

## Step 4: Generate Visualizations

```bash
python3 scripts/create_visualizations.py --data-dir data --forecast-file data/forecasts.parquet
```

## Step 5: Generate Narrative Brief

```bash
python3 scripts/evaluate_narratives.py --forecast-input data/forecasts.parquet --output reports/narrative_brief.md
```

## Alternative: Run Full Pipeline

```bash
python3 scripts/run_full_pipeline.py
```

This will execute all steps automatically.

## After Running

Once the pipeline completes:

1. Review forecast outputs in `data/forecasts.parquet`
2. Check visualizations in `reports/figures/`
3. Read narrative brief in `reports/narrative_brief.md`
4. Update article (`reports/article_draft.md`) with actual results from the forecasts

