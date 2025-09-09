import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Create outputs directory if it doesn't exist
os.makedirs('outputs', exist_ok=True)

# Load and examine the data
print("Loading datasets...")
fear_greed = pd.read_csv('csv_files/fear_greed_index.csv')
trading_data = pd.read_csv('csv_files/historical_data.csv')

print(f"Fear & Greed Index: {len(fear_greed)} records")
print(f"Trading Data: {len(trading_data)} records")

# Basic data info
print("\nFear & Greed Index columns:", fear_greed.columns.tolist())
print("Trading Data columns:", trading_data.columns.tolist())

# Create basic visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 1. Fear & Greed Index distribution
axes[0,0].hist(fear_greed['value'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
axes[0,0].set_title('Fear & Greed Index Distribution', fontsize=14, fontweight='bold')
axes[0,0].set_xlabel('Index Value (0-100)')
axes[0,0].set_ylabel('Frequency')
axes[0,0].grid(True, alpha=0.3)

# 2. Sentiment classification counts
sentiment_counts = fear_greed['classification'].value_counts()
colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
axes[0,1].bar(sentiment_counts.index, sentiment_counts.values, color=colors[:len(sentiment_counts)])
axes[0,1].set_title('Market Sentiment Distribution', fontsize=14, fontweight='bold')
axes[0,1].set_ylabel('Number of Days')
axes[0,1].tick_params(axis='x', rotation=45)
axes[0,1].grid(True, alpha=0.3)

# 3. Trading volume analysis (convert to numeric first)
trading_data['Size USD'] = pd.to_numeric(trading_data['Size USD'], errors='coerce')
volume_stats = trading_data['Size USD'].describe()
axes[1,0].boxplot(trading_data['Size USD'].dropna())
axes[1,0].set_title('Trading Volume Distribution (USD)', fontsize=14, fontweight='bold')
axes[1,0].set_ylabel('Trade Size (USD)')
axes[1,0].grid(True, alpha=0.3)

# 4. PnL analysis
trading_data['Closed PnL'] = pd.to_numeric(trading_data['Closed PnL'], errors='coerce')
pnl_data = trading_data['Closed PnL'].dropna()
axes[1,1].hist(pnl_data, bins=50, alpha=0.7, color='green', edgecolor='black')
axes[1,1].set_title('Profit & Loss Distribution', fontsize=14, fontweight='bold')
axes[1,1].set_xlabel('Closed PnL')
axes[1,1].set_ylabel('Frequency')
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/comprehensive_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Create time series analysis
plt.figure(figsize=(15, 8))

# Convert date columns
fear_greed['date'] = pd.to_datetime(fear_greed['date'])
fear_greed_sorted = fear_greed.sort_values('date')

plt.subplot(2, 1, 1)
plt.plot(fear_greed_sorted['date'], fear_greed_sorted['value'], linewidth=2, color='blue', alpha=0.8)
plt.fill_between(fear_greed_sorted['date'], fear_greed_sorted['value'], alpha=0.3, color='blue')
plt.title('Bitcoin Fear & Greed Index Over Time', fontsize=16, fontweight='bold')
plt.ylabel('Fear & Greed Index')
plt.grid(True, alpha=0.3)

# Add sentiment zones
plt.axhline(y=25, color='red', linestyle='--', alpha=0.7, label='Extreme Fear')
plt.axhline(y=75, color='green', linestyle='--', alpha=0.7, label='Extreme Greed')
plt.legend()

# Trading activity over time
trading_data['Timestamp IST'] = pd.to_datetime(trading_data['Timestamp IST'], format='%d-%m-%Y %H:%M', errors='coerce')
trading_data['Date'] = trading_data['Timestamp IST'].dt.date
daily_volume = trading_data.groupby('Date')['Size USD'].sum().reset_index()
daily_volume['Date'] = pd.to_datetime(daily_volume['Date'])

plt.subplot(2, 1, 2)
plt.plot(daily_volume['Date'], daily_volume['Size USD'], linewidth=2, color='orange', alpha=0.8)
plt.fill_between(daily_volume['Date'], daily_volume['Size USD'], alpha=0.3, color='orange')
plt.title('Daily Trading Volume', fontsize=16, fontweight='bold')
plt.ylabel('Volume (USD)')
plt.xlabel('Date')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/time_series_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Create summary statistics
print("\n=== ANALYSIS SUMMARY ===")
print(f"Fear & Greed Index Range: {fear_greed['value'].min()} - {fear_greed['value'].max()}")
print(f"Most Common Sentiment: {fear_greed['classification'].mode().iloc[0]}")
print(f"Average Fear & Greed Value: {fear_greed['value'].mean():.1f}")

print(f"\nTrading Data Summary:")
print(f"Total Trades: {len(trading_data):,}")
print(f"Unique Traders: {trading_data['Account'].nunique()}")
print(f"Total Volume: ${trading_data['Size USD'].sum():,.0f}")
print(f"Average Trade Size: ${trading_data['Size USD'].mean():.2f}")

profitable_trades = pnl_data[pnl_data > 0]
print(f"Profitable Trades: {len(profitable_trades)} ({len(profitable_trades)/len(pnl_data)*100:.1f}%)")

print("\nVisualizations created successfully!")
print("Files generated:")
print("- outputs/comprehensive_analysis.png")
print("- outputs/time_series_analysis.png")
