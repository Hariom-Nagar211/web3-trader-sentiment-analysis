import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
print("Loading data...")
fear_greed = pd.read_csv('csv_files/fear_greed_index.csv')
trading_data = pd.read_csv('csv_files/historical_data.csv')

# Basic preprocessing
fear_greed['date'] = pd.to_datetime(fear_greed['date'])
trading_data['Timestamp IST'] = pd.to_datetime(trading_data['Timestamp IST'], format='%d-%m-%Y %H:%M', errors='coerce')
trading_data['Date'] = trading_data['Timestamp IST'].dt.date
trading_data['Date'] = pd.to_datetime(trading_data['Date'])

# Convert numeric columns
numeric_cols = ['Execution Price', 'Size Tokens', 'Size USD', 'Closed PnL', 'Fee']
for col in numeric_cols:
    trading_data[col] = pd.to_numeric(trading_data[col], errors='coerce')

# Create sample visualizations
print("Creating visualizations...")

# 1. Fear & Greed distribution
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.hist(fear_greed['value'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
plt.title('Fear & Greed Index Distribution')
plt.xlabel('Index Value')
plt.ylabel('Frequency')

plt.subplot(2, 2, 2)
fear_greed['classification'].value_counts().plot(kind='bar', color='lightcoral')
plt.title('Market Sentiment Categories')
plt.xticks(rotation=45)
plt.ylabel('Count')

# 3. Trading volume over time (sample)
plt.subplot(2, 2, 3)
daily_volume = trading_data.groupby('Date')['Size USD'].sum().reset_index()
plt.plot(daily_volume['Date'], daily_volume['Size USD'], alpha=0.7, color='green')
plt.title('Daily Trading Volume')
plt.xticks(rotation=45)
plt.ylabel('Volume (USD)')

# 4. PnL distribution
plt.subplot(2, 2, 4)
pnl_data = trading_data['Closed PnL'].dropna()
plt.hist(pnl_data, bins=50, alpha=0.7, color='orange', edgecolor='black')
plt.title('PnL Distribution')
plt.xlabel('Closed PnL')
plt.ylabel('Frequency')

plt.tight_layout()
plt.savefig('outputs/sample_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Create correlation analysis
print("Creating correlation analysis...")
daily_stats = trading_data.groupby('Date').agg({
    'Size USD': 'sum',
    'Closed PnL': 'sum',
    'Account': 'nunique'
}).reset_index()

daily_stats.columns = ['Date', 'Total_Volume', 'Total_PnL', 'Unique_Traders']

# Merge with fear & greed
merged = pd.merge(fear_greed, daily_stats, left_on='date', right_on='Date', how='inner')

if len(merged) > 0:
    corr_data = merged[['value', 'Total_Volume', 'Total_PnL', 'Unique_Traders']].corr()
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_data, annot=True, cmap='RdYlBu_r', center=0, square=True, fmt='.3f')
    plt.title('Correlation: Market Sentiment vs Trading Metrics')
    plt.tight_layout()
    plt.savefig('outputs/correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

print("Analysis complete! Check outputs/ folder for visualizations.")
print(f"Fear & Greed data: {len(fear_greed)} records from {fear_greed['date'].min()} to {fear_greed['date'].max()}")
print(f"Trading data: {len(trading_data)} records from {trading_data['Date'].min()} to {trading_data['Date'].max()}")
print(f"Merged data: {len(merged) if 'merged' in locals() else 0} overlapping days")
