# Supplementary Materials

## A. Code Availability

All code for this project is available at: [REPOSITORY URL]

The repository includes:
- Data collection scripts (`scripts/collect_data.py`)
- Dataset building pipeline (`scripts/build_dataset.py`)
- Forecasting pipeline (`scripts/run_forecasts.py`)
- Visualization generation (`scripts/create_visualizations.py`)
- Narrative synthesis utilities (`utils/storytelling.py`)
- Complete pipeline runner (`scripts/run_full_pipeline.py`)

### Key Dependencies

- `statsforecast>=1.5.0`
- `neuralforecast>=1.6.0`
- `pandas>=2.0.0`
- `numpy>=1.24.0`
- `matplotlib>=3.7.0`
- `yfinance>=0.2.0`
- `pandas-datareader>=0.10.0`

### Installation

```bash
pip install -r requirements.txt
```

### Usage

See `EXECUTE_PIPELINE.md` for detailed instructions on running the complete pipeline.

## B. Data Availability Statement

### Primary Data Sources

1. Commodities   - Gold prices: FRED API (GOLDAMGBD228NLBM) or yfinance (GC=F)
   - Crude oil: FRED API (DCOILBRENTEU) or yfinance (BZ=F)

2. Macroeconomic Indicators   - CPI inflation: FRED API (CPIAUCSL), year-over-year percentage change
   - Consumer sentiment: FRED API (UMCSENT) or synthetic generation

3. Cultural Indicators   - Film releases: Synthetic data based on industry patterns (2010-present)
   - Book sales: Synthetic data based on industry patterns (2010-present)

4. Infrastructure   - Amtrak ridership: Aggregated from station-level data (2010-present)

### Data Access

- FRED Data: Available at https://fred.stlouisfed.org/ (free, no API key required)
- yfinance Data: Available via Python package `yfinance` (free, public APIs)
- Amtrak Data: Available in project repository at `data/amtrak_ridership_time_series_data.csv`
- Synthetic Data: Generated using reproducible random seeds (see code for details)

### Data Processing

All datasets are standardized to:
- Monthly frequency
- Schema: `[unique_id, ds, y]`
- Date range: 2010-01-01 to present (or latest available)

### Reproducibility

To reproduce the exact datasets used in this study:
1. Run `scripts/collect_data.py --datasets all` with the same date range
2. Synthetic data uses fixed random seeds (42, 43, 44, 45) for reproducibility
3. All data processing steps are documented in `scripts/build_dataset.py`

## C. Model Specifications

### AutoARIMA

Implementation: StatsForecast AutoARIMA

Parameter Search Space:
- p, q: [0, 5]
- d: [0, 2]
- P, Q: [0, 2]
- D: [0, 1]
- Seasonal period: 12 (monthly data)

Selection Criteria: AIC (Akaike Information Criterion)

Training: Fit on full historical data up to forecast start date

### SeasonalNaive

Implementation: StatsForecast SeasonalNaive

Method: Forecasts using value from same season in previous year

Seasonal Period: 12 months

Use Case: Baseline model for comparison

### NHITS

Implementation: NeuralForecast NHITS

Architecture:
- Input size: 24 months
- Horizon: 24 months
- Hidden units: [512, 512, 512]
- Number of stacks: 3
- Number of blocks per stack: 2

Training:
- Learning rate: 1e-3
- Batch size: 32
- Epochs: 50 (early stopping with patience=10)
- Optimizer: Adam
- Loss function: MAE

Hardware: Trained on CPU (GPU optional but not required)

## D. Additional Results

### Forecast Accuracy by Domain

[To be populated after running forecasts]

### Cross-Domain Correlations

[To be populated after running forecasts]

### Scenario Analysis

[To be populated after running forecasts]

## E. Ethical Considerations

### Data Privacy

- All datasets used are publicly available or synthetic
- No personally identifiable information is included
- Amtrak data is aggregated at the station level

### Reproducibility

- All code is open source
- Random seeds are fixed for synthetic data generation
- Data collection scripts document all sources

### Limitations

- Synthetic cultural data (film releases, book sales) may not reflect actual industry trends
- Forecasts are probabilistic and should not be interpreted as certainties
- Models assume stationarity and may not capture structural breaks

## F. Author Contributions

[To be filled in by authors]

## G. Acknowledgments

[To be filled in by authors]

## H. Funding Statement

[To be filled in by authors]

