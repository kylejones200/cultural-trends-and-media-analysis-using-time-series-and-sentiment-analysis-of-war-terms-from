# Code Availability Statement

## Repository Structure

```
chronotopes_of_culture/
├── scripts/
│   ├── collect_data.py          # Data collection from APIs
│   ├── build_dataset.py          # Master dataset construction
│   ├── run_forecasts.py          # Forecasting pipeline
│   ├── create_visualizations.py  # Figure generation
│   ├── evaluate_narratives.py    # Narrative synthesis
│   └── run_full_pipeline.py      # End-to-end execution
├── utils/
│   ├── loaders.py                # Data loading utilities
│   ├── feature_pipeline.py       # Data harmonization
│   └── storytelling.py           # Narrative generation
├── notebooks/
│   └── 01_data_scraping.ipynb    # Exploratory analysis
├── data/
│   ├── external/                 # Raw collected data
│   ├── intermediate/             # Processed datasets
│   └── master_dataset.parquet    # Unified dataset
└── reports/
    ├── figures/                  # Generated visualizations
    └── narrative_brief.md       # Forecast narratives
```

## Installation

```bash
# Clone repository
git clone [REPOSITORY_URL]
cd chronotopes_of_culture

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```bash
# Run complete pipeline
python scripts/run_full_pipeline.py

# Or run steps individually
python scripts/collect_data.py --datasets all
python scripts/build_dataset.py
python scripts/run_forecasts.py --horizon 24
python scripts/create_visualizations.py
```

## Key Functions

### Data Collection

```python
from scripts.collect_data import fetch_gold_prices, fetch_oil_prices

# Fetch gold prices
gold = fetch_gold_prices(start_date="2010-01-01")

# Fetch oil prices
oil = fetch_oil_prices(start_date="2010-01-01")
```

### Forecasting

```python
from scripts.run_forecasts import run_statsforecast, run_neuralforecast

# Run StatsForecast models
forecasts_sf = run_statsforecast(df, horizon=24)

# Run NeuralForecast models
forecasts_nf = run_neuralforecast(df, horizon=24)
```

### Visualization

```python
from scripts.create_visualizations import plot_forecasts

# Plot forecasts
plot_forecasts(historical, forecasts, output_path)
```

## License

[To be specified by authors]

## Citation

If you use this code, please cite:

```
[Citation to be added after publication]
```

## Contact

For questions or issues, please open an issue on the repository or contact [EMAIL].

