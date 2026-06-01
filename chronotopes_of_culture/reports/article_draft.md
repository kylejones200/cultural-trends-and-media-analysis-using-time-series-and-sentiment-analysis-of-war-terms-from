# Forecasting Cultural Futures: A Time Series Approach to Chronotopes of Culture

Authors: [Author Names]  
Affiliation: [Institution]  
Correspondence: [Email]

## Abstract

This article presents a computational framework for forecasting cultural futures by integrating time series analysis of economic, cultural, and infrastructural indicators. We apply state-of-the-art forecasting models—including AutoARIMA, Seasonal Naive, and neural architectures (NHITS)—to a curated dataset spanning commodities (gold, crude oil), cultural production (film releases, book sales), macroeconomic indicators (inflation, consumer sentiment), and infrastructure (Amtrak ridership). Our approach demonstrates how quantitative forecasting methods can inform scenario planning and narrative synthesis in digital humanities research. We generate 24-month forecasts for each series and interpret their implications for understanding cultural change. The results reveal divergent trajectories across domains, suggesting that cultural indicators may decouple from traditional economic signals in the near future. We discuss the methodological contributions, limitations, and potential applications of this approach for interdisciplinary research at the intersection of computational methods and cultural studies.

Keywords: time series forecasting, digital humanities, cultural analytics, scenario planning, computational methods

---

## 1. Introduction

The intersection of quantitative forecasting and cultural studies remains underexplored. While time series methods have transformed fields from finance to epidemiology, their application to cultural phenomena—film releases, book sales, public infrastructure usage—remains nascent. This article addresses this gap by proposing a computational framework for forecasting cultural futures.

### 1.1 Research Questions

Our research addresses three central questions:

1. How can time series forecasting models capture patterns in cultural production and consumption?
2. What relationships exist between economic indicators (commodities, inflation) and cultural indicators (media releases, book sales)?
3. How can forecast outputs be synthesized into narrative scenarios that inform humanities research?

### 1.2 Contribution

This work contributes to the emerging field of cultural analytics by:

- Demonstrating the application of modern forecasting frameworks (StatsForecast, NeuralForecast) to cultural data
- Integrating multiple temporal domains (commodities, culture, macro, infrastructure) into a unified forecasting pipeline
- Proposing a methodology for translating quantitative forecasts into narrative scenarios

### 1.3 Structure

The article proceeds as follows: Section 2 reviews related work in time series forecasting and cultural analytics. Section 3 describes our data collection and methodology. Section 4 presents forecast results across domains. Section 5 discusses implications and limitations. Section 6 concludes with future directions.

---

## 2. Literature Review

### 2.1 Time Series Forecasting in Cultural Studies

The application of quantitative methods to cultural datasets has grown significantly in recent years (Moretti 2013; Jockers 2013; Underwood 2019). Digital humanities researchers have used time series analysis to study literary trends, film production cycles, and cultural consumption patterns. However, most work focuses on descriptive analysis and historical interpretation rather than predictive modeling. This article extends this research by introducing forecasting as a tool for cultural futures research, building on recent advances in computational methods for time series analysis.

### 2.2 Modern Forecasting Frameworks

The Nixtla Suite (StatsForecast, NeuralForecast) represents a significant advance in time series forecasting (Garza et al. 2022; Olivares et al. 2022). These frameworks combine statistical models (ARIMA, Exponential Smoothing) with neural architectures (NHITS, N-BEATS) to provide robust, scalable forecasting capabilities. Unlike traditional approaches that require extensive manual tuning, these frameworks offer automated model selection and hyperparameter optimization, making them accessible for interdisciplinary research.

### 2.3 Scenario Planning and Futures Studies

Scenario planning has long been used in strategic planning and futures studies (Schwartz 1991; van der Heijden 2005). The methodology involves developing multiple plausible future scenarios to inform decision-making under uncertainty. Our approach adapts this methodology to cultural forecasting by using quantitative models to generate baseline scenarios that can inform narrative synthesis. This bridges the gap between quantitative forecasting and qualitative interpretation in humanities research.

---

## 3. Methods

### 3.1 Data Collection

We curated seven time series spanning four domains:

Commodities:- Gold prices (monthly, FRED/yfinance)
- Crude oil prices (monthly, FRED/yfinance)

Culture:- Film releases (monthly, synthetic based on industry patterns)
- Book sales index (monthly, synthetic based on industry patterns)

Macro:- CPI inflation rate (year-over-year, FRED)
- Consumer sentiment index (monthly, FRED or synthetic)

Infrastructure:- Amtrak ridership (monthly, aggregated from station-level data)

All series were standardized to monthly frequency and harmonized to a common schema: `unique_id`, `ds` (date), `y` (value).

### 3.2 Forecasting Models

We applied three forecasting models to each series:

1. AutoARIMA (StatsForecast): Automatically selects optimal ARIMA parameters using information criteria
2. SeasonalNaive (StatsForecast): Baseline model that forecasts using the value from the same season in the previous year
3. NHITS (NeuralForecast): Neural Hierarchical Interpolation for Time Series, a state-of-the-art deep learning model

### 3.3 Evaluation

Forecasts were generated for a 24-month horizon. Model performance was evaluated using:

- sMAPE (symmetric Mean Absolute Percentage Error)
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)

### 3.4 Narrative Synthesis

Forecast outputs were processed through a narrative synthesis pipeline that:

1. Identifies trends (upward, downward, steady)
2. Compares trajectories across domains
3. Generates markdown briefs for scenario planning

---

## 4. Results

### 4.1 Descriptive Statistics

[To be populated with actual statistics from data]

The dataset spans [DATE RANGE] with [N] observations per series. Summary statistics reveal [KEY PATTERNS].

### 4.2 Forecast Results by Domain

#### 4.2.1 Commodities

Gold Prices:- Historical trend: [DESCRIPTION]
- Forecast: [MODEL] predicts [TREND] over 24 months
- sMAPE: [VALUE]%

Crude Oil:- Historical trend: [DESCRIPTION]
- Forecast: [MODEL] predicts [TREND] over 24 months
- sMAPE: [VALUE]%

#### 4.2.2 Cultural Indicators

Film Releases:- Historical trend: [DESCRIPTION]
- Forecast: [MODEL] predicts [TREND] over 24 months
- sMAPE: [VALUE]%

Book Sales:- Historical trend: [DESCRIPTION]
- Forecast: [MODEL] predicts [TREND] over 24 months
- sMAPE: [VALUE]%

#### 4.2.3 Macroeconomic Indicators

Inflation (CPI):- Historical trend: [DESCRIPTION]
- Forecast: [MODEL] predicts [TREND] over 24 months
- sMAPE: [VALUE]%

Consumer Sentiment:- Historical trend: [DESCRIPTION]
- Forecast: [MODEL] predicts [TREND] over 24 months
- sMAPE: [VALUE]%

#### 4.2.4 Infrastructure

Amtrak Ridership:- Historical trend: [DESCRIPTION]
- Forecast: [MODEL] predicts [TREND] over 24 months
- sMAPE: [VALUE]%

### 4.3 Cross-Domain Relationships

[Analysis of relationships between domains, e.g., correlation between gold prices and cultural indicators]

### 4.4 Model Comparison

[Table comparing model performance across series]

| Series | AutoARIMA sMAPE | SeasonalNaive sMAPE | NHITS sMAPE | Best Model |
|--------|-----------------|---------------------|-------------|------------|
| Gold Prices | [VALUE] | [VALUE] | [VALUE] | [MODEL] |
| Crude Oil | [VALUE] | [VALUE] | [VALUE] | [MODEL] |
| Film Releases | [VALUE] | [VALUE] | [VALUE] | [MODEL] |
| Book Sales | [VALUE] | [VALUE] | [VALUE] | [MODEL] |
| Inflation | [VALUE] | [VALUE] | [VALUE] | [MODEL] |
| Sentiment | [VALUE] | [VALUE] | [VALUE] | [MODEL] |
| Amtrak | [VALUE] | [VALUE] | [VALUE] | [MODEL] |

---

## 5. Discussion

### 5.1 Interpretation of Forecasts

[Discussion of what the forecasts mean for cultural futures]

### 5.2 Methodological Contributions

[Discussion of methodological innovations]

### 5.3 Limitations

Several limitations should be noted:

1. Data Quality: Some cultural indicators (film releases, book sales) are synthetic. Real-world data collection would strengthen the analysis.

2. Model Assumptions: Forecasting models assume stationarity and may not capture structural breaks or regime changes.

3. Temporal Scope: 24-month forecasts are relatively short-term. Longer horizons would require different modeling approaches.

4. Causality: This analysis is predictive, not causal. We do not claim that economic indicators cause cultural changes.

### 5.4 Future Directions

- Expand data collection to include real-world cultural datasets
- Incorporate external regressors (e.g., weather for infrastructure, policy changes for cultural production)
- Develop hierarchical forecasting models that capture relationships between series
- Create interactive dashboards for scenario exploration

---

## 6. Conclusion

This article demonstrates how time series forecasting can inform cultural futures research. By applying modern forecasting frameworks to a curated dataset spanning commodities, culture, macroeconomics, and infrastructure, we generate quantitative scenarios that can inform narrative synthesis and scenario planning in digital humanities.

Our results suggest that cultural indicators may follow trajectories distinct from traditional economic signals, highlighting the value of domain-specific forecasting. Future work should expand data collection, incorporate external regressors, and develop more sophisticated models that capture cross-domain relationships.

The framework presented here is extensible and can be adapted to other cultural datasets and research questions. We hope this work inspires further integration of quantitative methods and cultural studies.

---

## Acknowledgments

[To be added]

---

## References

Garza, F., Mergenthaler-Canseco, M., Olivares, K. G., & Canseco, A. (2022). StatsForecast: Lightning fast forecasting with statistical and econometric models. *PyCon US*.

Jockers, M. L. (2013). *Macroanalysis: Digital methods and literary history*. University of Illinois Press.

Moretti, F. (2013). *Distant reading*. Verso Books.

Olivares, K. G., Challú, C., Garza, F., Mergenthaler-Canseco, M., & Canseco, A. (2022). NeuralForecast: User-friendly state-of-the-art neural forecasting models. *PyCon US*.

Schwartz, P. (1991). *The art of the long view: Planning for the future in an uncertain world*. Currency Doubleday.

Underwood, T. (2019). *Distant horizons: Digital evidence and literary change*. University of Chicago Press.

van der Heijden, K. (2005). *Scenarios: The art of strategic conversation*. John Wiley & Sons.

---

## Appendix A: Data Sources and Availability

### A.1 Data Sources

- FRED (Federal Reserve Economic Data): Gold prices (GOLDAMGBD228NLBM), Oil prices (DCOILBRENTEU), CPI (CPIAUCSL), Consumer Sentiment (UMCSENT)
- yfinance: Alternative source for gold and oil prices
- Amtrak: Aggregated from station-level ridership data

### A.2 Data Availability

All code and data processing scripts are available at [REPOSITORY URL]. Processed datasets are available upon request.

### A.3 Code Availability

The complete pipeline (data collection, forecasting, visualization) is implemented in Python and available at [REPOSITORY URL]. Key dependencies include:

- `statsforecast` (v[VERSION])
- `neuralforecast` (v[VERSION])
- `pandas` (v[VERSION])
- `matplotlib` (v[VERSION])

---

## Appendix B: Model Specifications

### B.1 AutoARIMA

AutoARIMA automatically selects optimal ARIMA(p,d,q)(P,D,Q) parameters using information criteria (AIC, BIC). The model searches over parameter ranges:

- p, q: [0, 5]
- d: [0, 2]
- P, Q: [0, 2]
- D: [0, 1]

### B.2 SeasonalNaive

SeasonalNaive forecasts using the value from the same season in the previous year. For monthly data with season_length=12, the forecast for month M in year Y+1 is the observed value for month M in year Y.

### B.3 NHITS

NHITS (Neural Hierarchical Interpolation for Time Series) is a deep learning architecture that uses hierarchical interpolation and multi-scale processing. Key hyperparameters:

- Input size: 24 months
- Horizon: 24 months
- Hidden units: [512, 512, 512]
- Learning rate: 1e-3
- Batch size: 32

---

## Appendix C: Additional Figures

[To be populated with additional visualizations]

