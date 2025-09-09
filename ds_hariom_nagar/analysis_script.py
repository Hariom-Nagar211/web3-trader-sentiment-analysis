#!/usr/bin/env python3
"""
Web3 Trading Analysis: Trader Behavior vs Market Sentiment
Author: Hariom Nagar
Date: September 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('default')
sns.set_palette('husl')

def load_and_preprocess_data():
    """Load and preprocess the datasets"""
    print("Loading datasets...")
    
    # Load datasets
    fear_greed = pd.read_csv('csv_files/fear_greed_index.csv')
    trading_data = pd.read_csv('csv_files/historical_data.csv')
    
    print(f"Fear & Greed Index shape: {fear_greed.shape}")
    print(f"Trading Data shape: {trading_data.shape}")
    
    # Clean Fear & Greed data
    fear_greed['date'] = pd.to_datetime(fear_greed['date'])
    fear_greed = fear_greed.sort_values('date')
    
    # Clean Trading data
    trading_data['Timestamp IST'] = pd.to_datetime(trading_data['Timestamp IST'], format='%d-%m-%Y %H:%M')
    trading_data['Date'] = trading_data['Timestamp IST'].dt.date
    trading_data['Date'] = pd.to_datetime(trading_data['Date'])
    
    # Clean numeric columns
    numeric_cols = ['Execution Price', 'Size Tokens', 'Size USD', 'Closed PnL', 'Fee']
    for col in numeric_cols:
        trading_data[col] = pd.to_numeric(trading_data[col], errors='coerce')
    
    return fear_greed, trading_data

def create_eda_visualizations(fear_greed, trading_data):
    """Create exploratory data analysis visualizations"""
    print("Creating EDA visualizations...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Distribution of Fear & Greed values
    axes[0,0].hist(fear_greed['value'], bins=30, alpha=0.7, color='skyblue')
    axes[0,0].set_title('Distribution of Fear & Greed Index Values')
    axes[0,0].set_xlabel('Index Value')
    axes[0,0].set_ylabel('Frequency')
    
    # Classification counts
    fear_greed['classification'].value_counts().plot(kind='bar', ax=axes[0,1], color='lightcoral')
    axes[0,1].set_title('Fear & Greed Classifications')
    axes[0,1].set_xlabel('Classification')
    axes[0,1].set_ylabel('Count')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # Time series of Fear & Greed Index
    axes[1,0].plot(fear_greed['date'], fear_greed['value'], alpha=0.7, color='green')
    axes[1,0].set_title('Fear & Greed Index Over Time')
    axes[1,0].set_xlabel('Date')
    axes[1,0].set_ylabel('Index Value')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # Trading volume over time
    daily_volume = trading_data.groupby('Date')['Size USD'].sum().reset_index()
    axes[1,1].plot(daily_volume['Date'], daily_volume['Size USD'], alpha=0.7, color='orange')
    axes[1,1].set_title('Daily Trading Volume (USD)')
    axes[1,1].set_xlabel('Date')
    axes[1,1].set_ylabel('Volume (USD)')
    axes[1,1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('outputs/eda_overview.png', dpi=300, bbox_inches='tight')
    plt.close()

def merge_and_analyze_correlation(fear_greed, trading_data):
    """Merge datasets and perform correlation analysis"""
    print("Merging datasets and analyzing correlations...")
    
    # Aggregate trading data by date
    daily_trading_stats = trading_data.groupby('Date').agg({
        'Size USD': ['sum', 'mean', 'count'],
        'Closed PnL': ['sum', 'mean'],
        'Account': 'nunique',
        'Execution Price': 'mean'
    }).round(2)
    
    # Flatten column names
    daily_trading_stats.columns = ['_'.join(col).strip() for col in daily_trading_stats.columns]
    daily_trading_stats = daily_trading_stats.reset_index()
    
    # Rename columns for clarity
    daily_trading_stats.columns = ['Date', 'Total_Volume_USD', 'Avg_Trade_Size_USD', 'Trade_Count', 
                                  'Total_PnL', 'Avg_PnL', 'Unique_Traders', 'Avg_Price']
    
    # Merge with fear & greed data
    merged_data = pd.merge(fear_greed, daily_trading_stats, left_on='date', right_on='Date', how='inner')
    
    print(f"Merged dataset shape: {merged_data.shape}")
    
    # Correlation analysis
    correlation_cols = ['value', 'Total_Volume_USD', 'Avg_Trade_Size_USD', 'Trade_Count', 
                       'Total_PnL', 'Avg_PnL', 'Unique_Traders', 'Avg_Price']
    
    correlation_matrix = merged_data[correlation_cols].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='RdYlBu_r', center=0, 
                square=True, fmt='.3f', cbar_kws={'shrink': 0.8})
    plt.title('Correlation Matrix: Market Sentiment vs Trading Metrics', fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig('outputs/correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return merged_data, correlation_matrix

def analyze_sentiment_patterns(merged_data):
    """Analyze trading patterns by sentiment"""
    print("Analyzing sentiment-based trading patterns...")
    
    # Visualize trading patterns by sentiment
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Volume by sentiment
    sns.boxplot(data=merged_data, x='classification', y='Total_Volume_USD', ax=axes[0,0])
    axes[0,0].set_title('Trading Volume by Market Sentiment')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # Trade count by sentiment
    sns.boxplot(data=merged_data, x='classification', y='Trade_Count', ax=axes[0,1])
    axes[0,1].set_title('Number of Trades by Market Sentiment')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # PnL by sentiment
    sns.boxplot(data=merged_data, x='classification', y='Total_PnL', ax=axes[0,2])
    axes[0,2].set_title('Total PnL by Market Sentiment')
    axes[0,2].tick_params(axis='x', rotation=45)
    
    # Unique traders by sentiment
    sns.boxplot(data=merged_data, x='classification', y='Unique_Traders', ax=axes[1,0])
    axes[1,0].set_title('Unique Traders by Market Sentiment')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # Average trade size by sentiment
    sns.boxplot(data=merged_data, x='classification', y='Avg_Trade_Size_USD', ax=axes[1,1])
    axes[1,1].set_title('Average Trade Size by Market Sentiment')
    axes[1,1].tick_params(axis='x', rotation=45)
    
    # Average PnL by sentiment
    sns.boxplot(data=merged_data, x='classification', y='Avg_PnL', ax=axes[1,2])
    axes[1,2].set_title('Average PnL by Market Sentiment')
    axes[1,2].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('outputs/sentiment_trading_patterns.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Generate summary statistics
    sentiment_stats = merged_data.groupby('classification').agg({
        'Total_Volume_USD': ['mean', 'std'],
        'Trade_Count': ['mean', 'std'],
        'Total_PnL': ['mean', 'std'],
        'Unique_Traders': ['mean', 'std'],
        'value': ['mean', 'min', 'max']
    }).round(2)
    
    return sentiment_stats

def generate_insights(correlation_matrix, sentiment_stats):
    """Generate key insights from the analysis"""
    print("Generating insights...")
    
    insights = []
    
    # Correlation insights
    fear_greed_corr = correlation_matrix.loc['value'].drop('value')
    strongest_corr = fear_greed_corr.abs().idxmax()
    strongest_corr_value = fear_greed_corr[strongest_corr]
    
    insights.append(f"Strongest correlation with Fear & Greed Index: {strongest_corr} ({strongest_corr_value:.3f})")
    
    # Sentiment-based insights
    volume_by_sentiment = sentiment_stats['Total_Volume_USD']['mean'].sort_values(ascending=False)
    insights.append(f"Highest average trading volume during: {volume_by_sentiment.index[0]} periods")
    
    pnl_by_sentiment = sentiment_stats['Total_PnL']['mean'].sort_values(ascending=False)
    insights.append(f"Most profitable sentiment period: {pnl_by_sentiment.index[0]} periods")
    
    return insights

def main():
    """Main analysis pipeline"""
    print("Starting Web3 Trading Analysis...")
    
    # Load and preprocess data
    fear_greed, trading_data = load_and_preprocess_data()
    
    # Create EDA visualizations
    create_eda_visualizations(fear_greed, trading_data)
    
    # Merge datasets and analyze correlations
    merged_data, correlation_matrix = merge_and_analyze_correlation(fear_greed, trading_data)
    
    # Analyze sentiment patterns
    sentiment_stats = analyze_sentiment_patterns(merged_data)
    
    # Generate insights
    insights = generate_insights(correlation_matrix, sentiment_stats)
    
    # Save results
    merged_data.to_csv('csv_files/merged_analysis_data.csv', index=False)
    sentiment_stats.to_csv('csv_files/sentiment_statistics.csv')
    
    print("\nKey Insights:")
    for insight in insights:
        print(f"- {insight}")
    
    print("\nAnalysis complete! Check the outputs/ folder for visualizations.")

if __name__ == "__main__":
    main()
