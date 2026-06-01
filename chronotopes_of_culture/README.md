# Chronotopes of Culture

Forecasting cultural futures by weaving together quantitative time-series models and narrative interpretation. This project consolidates commodity, cultural, and macroeconomic signals into a reproducible research spine suitable for publication, classroom use, and public storytelling.

## Structure

- `data_catalog.yaml` — curated list of datasets and APIs used in the forecasting workflows.
- `notebooks/` — exploratory and production notebooks (data ingestion, feature engineering, scenario analysis, narrative dashboards).
- `scripts/` — command-line utilities for building datasets, running forecasts, and compiling narrative assets.
- `utils/` — shared helper modules (loaders, feature pipelines, storytelling helpers).
- `reports/` — whitepaper drafts, figures, and exported interactive assets.

## Vision

1. Curate temporal datasets that capture cultural, economic, and environmental signals (commodities, sentiment, cultural production metrics, macro indicators).
2. Forecast multiple futures using classical, machine learning, and neural approaches (leveraging the template suite in this repo).
3. Interpret and narrate the results through essays, dashboards, and speculative scenarios aimed at scholarly and public audiences.

## Getting Started

### Quick Start (Full Pipeline)

Run the complete pipeline from data collection to visualization:

```bash
pip install -r requirements.txt
python scripts/run_full_pipeline.py
```

This will:
1. Collect data from FRED, yfinance, and generate synthetic cultural data
2. Build the master dataset
3. Run forecasts using AutoARIMA, SeasonalNaive, and NHITS
4. Generate visualizations
5. Create narrative briefs

### Step-by-Step

Alternatively, run each step individually:

```bash
# 1. Collect data
python scripts/collect_data.py --datasets all

# 2. Build master dataset
python scripts/build_dataset.py --catalog data_catalog.yaml --output data/master_dataset.parquet

# 3. Run forecasts
python scripts/run_forecasts.py --input data/master_dataset.parquet --horizon 24 --output data/forecasts.parquet

# 4. Generate visualizations
python scripts/create_visualizations.py --data-dir data --forecast-file data/forecasts.parquet

# 5. Generate narrative brief
python scripts/evaluate_narratives.py --forecast-input data/forecasts.parquet --output reports/narrative_brief.md
```

Then open the notebooks in `notebooks/` to explore data stories and draft interpretive narratives.

## Publishing Targets

- Journal articles: *Journal of Cultural Analytics*, *Digital Scholarship in the Humanities*, *New Media & Society*.
- Public storytelling: interactive essays, museum/library exhibits, classroom modules.

## Status

### ✅ Completed
- [x] Project structure and infrastructure
- [x] Data catalog with standardized schema
- [x] Data collection scripts (FRED, yfinance, synthetic)
- [x] Forecasting pipeline (StatsForecast, NeuralForecast)
- [x] Visualization generation scripts
- [x] Narrative synthesis utilities
- [x] Article draft template
- [x] Completion plan (see `COMPLETION_PLAN.md`)

### 🚧 In Progress
- [ ] Data collection execution
- [ ] Forecast generation
- [ ] Article writing (draft exists, needs results)

### 📋 Next Steps
1. Run data collection: Execute `collect_data.py` to fetch real datasets
2. Run forecasts: Execute `run_forecasts.py` to generate predictions
3. Generate figures: Execute `create_visualizations.py` for publication-quality charts
4. Complete article: Fill in results sections in `reports/article_draft.md`
5. Submit for review: Target journals: *Journal of Cultural Analytics*, *Digital Scholarship in the Humanities*

See `COMPLETION_PLAN.md` for detailed timeline and methodology.

## Project Files

- `COMPLETION_PLAN.md` — Detailed plan for completing the article
- `reports/article_draft.md` — Academic article template (ready for results)
- `reports/cultural_futures_whitepaper.md` — Original project whitepaper
- `data_catalog.yaml` — Dataset definitions and metadata
- `scripts/` — All pipeline scripts (collect, build, forecast, visualize, narrate)
- `utils/` — Helper functions for loading, feature engineering, storytelling
