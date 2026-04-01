# Completion Plan: Chronotopes of Culture Article

## Current State Assessment

### ✅ What's Complete
- Project structure and infrastructure
- Scripts for data building, forecasting, and narrative evaluation
- Data catalog YAML structure
- Utility functions for loading, feature engineering, and storytelling
- Whitepaper outline

### ❌ What's Missing
- Actual data collection/ingestion
- Forecast outputs
- Visualizations and figures
- Complete academic article
- Supplementary materials

## Step-by-Step Completion Plan

### Phase 1: Data Collection (Priority 1)
**Goal**: Collect all required datasets and standardize them

1. **Gold Prices**
   - Source: FRED API (GOLDAMGBD228NLBM) or yfinance
   - Frequency: Monthly
   - Time range: 2010-present

2. **Crude Oil Prices**
   - Source: FRED API (DCOILBRENTEU) or yfinance
   - Frequency: Daily → aggregate to monthly
   - Time range: 2010-present

3. **Inflation (CPI)**
   - Source: FRED API (CPIAUCSL)
   - Frequency: Monthly
   - Time range: 2010-present

4. **Film Releases**
   - Source: Box Office Mojo API or web scraping
   - Alternative: Use synthetic data based on industry trends
   - Frequency: Weekly → aggregate to monthly
   - Time range: 2010-present

5. **Book Sales**
   - Source: NYT Bestseller API or synthetic data
   - Frequency: Monthly
   - Time range: 2010-present

6. **Sentiment Index**
   - Source: FRED (UMCSENT) or Twitter API
   - Alternative: Use economic sentiment indicators
   - Frequency: Monthly
   - Time range: 2010-present

7. **Amtrak Ridership**
   - ✅ Already available in data/intermediate/

### Phase 2: Data Pipeline Execution (Priority 2)
1. Run `build_dataset.py` to create master dataset
2. Validate data quality and handle missing values
3. Document any data limitations

### Phase 3: Forecasting (Priority 3)
1. Run `run_forecasts.py` with multiple models
2. Generate forecasts for 12-24 month horizon
3. Compare model performance
4. Select best models for each series

### Phase 4: Visualization (Priority 4)
1. Create time series plots for each variable
2. Generate forecast visualizations
3. Create comparison charts (commodities vs. culture)
4. Design "chronoscope" dashboard concept
5. Export publication-quality figures

### Phase 5: Article Writing (Priority 5)
1. **Introduction**
   - Context: Cultural forecasting and time series
   - Research questions
   - Contribution to digital humanities

2. **Literature Review**
   - Time series forecasting in cultural studies
   - Quantitative methods in digital humanities
   - Scenario planning and futures studies

3. **Methods**
   - Data sources and collection
   - Forecasting models (StatsForecast, NeuralForecast)
   - Evaluation metrics
   - Narrative synthesis approach

4. **Results**
   - Descriptive statistics
   - Forecast results by domain
   - Cross-domain relationships
   - Scenario analysis

5. **Discussion**
   - Interpretation of forecasts
   - Cultural implications
   - Limitations
   - Future directions

6. **Conclusion**
   - Summary of findings
   - Contribution to field
   - Practical applications

### Phase 6: Supplementary Materials (Priority 6)
1. Appendix with detailed model specifications
2. Code availability statement
3. Data availability statement
4. Additional figures and tables

## Target Journals

1. **Journal of Cultural Analytics** (Primary)
   - Focus: Computational methods in cultural studies
   - Format: LaTeX or Word
   - Length: 8,000-12,000 words

2. **Digital Scholarship in the Humanities** (Alternative)
   - Focus: Digital methods in humanities
   - Format: XML/HTML
   - Length: 6,000-10,000 words

3. **New Media & Society** (Alternative)
   - Focus: Media and technology
   - Format: Word
   - Length: 7,000-9,000 words

## Timeline Estimate

- Phase 1 (Data Collection): 2-3 days
- Phase 2 (Data Pipeline): 1 day
- Phase 3 (Forecasting): 1-2 days
- Phase 4 (Visualization): 2-3 days
- Phase 5 (Article Writing): 5-7 days
- Phase 6 (Supplements): 1-2 days

**Total: 12-18 days** for complete article-ready project

## Next Immediate Steps

1. Create data collection script using FRED API and yfinance
2. Update data catalog with actual data paths
3. Run initial forecasts
4. Generate first visualizations
5. Begin article draft

