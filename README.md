# Web3 Trading Analysis: Trader Behavior vs Market Sentiment

**Author:** Hariom Nagar  
**Assignment:** Data Science - Web3 Trading Team  
**Date:** September 2025

## 📋 Project Overview

This project analyzes the relationship between trader behavior and market sentiment using:
1. **Bitcoin Fear & Greed Index** - Market sentiment data
2. **Hyperliquid Historical Trading Data** - Individual trader transactions

## 🎯 Objective

Explore how trading behavior (profitability, risk, volume, leverage) aligns or diverges from overall market sentiment (fear vs greed) to identify hidden trends that could influence smarter trading strategies.

## 📁 Directory Structure

```
ds_hariom_nagar/
├── notebook_1.ipynb          # Main analysis notebook (Google Colab ready)
├── notebook_2.ipynb          # Advanced analysis continuation
├── analysis_script.py        # Python script for local execution
├── csv_files/                # Data storage
│   ├── fear_greed_index.csv   # Bitcoin Fear & Greed Index data
│   ├── historical_data.csv    # Hyperliquid trading data
│   ├── merged_analysis_data.csv # Processed merged dataset
│   └── sentiment_statistics.csv # Summary statistics by sentiment
├── outputs/                   # Generated visualizations
│   ├── eda_overview.png       # Exploratory data analysis charts
│   ├── correlation_matrix.png # Correlation heatmap
│   └── sentiment_trading_patterns.png # Trading patterns by sentiment
├── ds_report.pdf             # Final analysis report
└── README.md                 # This file
```

## 🚀 Setup Instructions

### Google Colab (Recommended)
1. Upload `notebook_1.ipynb` and `notebook_2.ipynb` to Google Colab
2. Upload the CSV files from `csv_files/` directory to Colab
3. Run all cells sequentially
4. Download generated visualizations to `outputs/` folder

### Local Setup
1. Install required packages:
   ```bash
   pip install pandas numpy matplotlib seaborn scipy scikit-learn
   ```
2. Run the analysis script:
   ```bash
   python analysis_script.py
   ```

## 📊 Key Analysis Components

### 1. Data Preprocessing
- Date alignment between datasets
- Numeric data cleaning and validation
- Missing value handling

### 2. Exploratory Data Analysis
- Fear & Greed Index distribution and trends
- Trading volume and activity patterns
- Temporal analysis of market behavior

### 3. Correlation Analysis
- Statistical relationships between sentiment and trading metrics
- Heatmap visualization of correlations
- Identification of strongest predictive factors

### 4. Sentiment-Based Trading Patterns
- Trading behavior during different market sentiments
- Volume, frequency, and profitability analysis
- Risk assessment by sentiment periods

## 🔍 Key Insights

The analysis reveals several important patterns:

1. **Volume Correlation**: Trading volume shows significant correlation with market sentiment
2. **Profitability Patterns**: Different sentiment periods exhibit distinct profitability characteristics
3. **Trader Behavior**: Risk-taking behavior varies significantly across fear/greed cycles
4. **Market Timing**: Optimal entry/exit points can be identified using sentiment indicators

## 📈 Visualizations Generated

1. **EDA Overview**: Distribution plots and time series analysis
2. **Correlation Matrix**: Heatmap showing relationships between variables
3. **Sentiment Patterns**: Box plots comparing trading metrics across sentiment categories

## 🎯 Business Applications

- **Risk Management**: Adjust position sizes based on market sentiment
- **Entry/Exit Timing**: Use sentiment indicators for better trade timing
- **Portfolio Optimization**: Balance aggressive/conservative strategies by sentiment
- **Market Making**: Adjust spreads and liquidity provision based on sentiment

## 📧 Contact

**Hariom Nagar**  
Email: [Your Email]  
Subject: "Junior Data Scientist – Trader Behavior Insights"

## 🔗 Google Colab Links

- **Main Analysis Notebook**: [Add Colab link here]
- **Advanced Analysis**: [Add Colab link here]

*Note: Ensure all Colab notebooks are set to 'Anyone with the link can view'*
