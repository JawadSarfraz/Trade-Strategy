# Trading Bot

📘 Binance Order Book Analysis - README

🚀 Project Overview

Project focuses on real-time order book tracking from Binance using WebSockets. Storing and analyzing order book data to detect market trends, liquidity shifts, and trading opportunities.

📡 Current Implementation

✅ 1. WebSocket Connection to Binance

Established a WebSocket connection to Binance Spot Order Book using the depth stream.

Subscribes to BTC/USDT (but can be extended to other pairs).

Continuously receives order book updates.

✅ 2. Order Book Storage (Rolling Buffer)

Stores the last 100 updates in a rolling buffer using collections.deque.

Each update consists of top 5 bid/ask levels, totaling 1000 data points.

Data is structured using Pandas DataFrames for easy analysis.

✅ 3. Computing the Bid-Ask Spread

Extracts the highest bid price and lowest ask price.

Computes the spread (Ask - Bid) to measure market liquidity.

Stores the spread history for trend analysis.

📊 Planned Next Steps

Now that we have 100 updates stored, we can extract meaningful trading insights.

🔥 1. Cumulative Volume Delta (CVD) Analysis

Measures market buying vs. selling pressure.

Tracks if more bids (buyers) or asks (sellers) dominate over time.

Use Case: Helps determine whether price is likely to rise (bullish) or fall (bearish).

⚖️ 2. Order Flow Imbalance Detection

Detects shifts in market sentiment by comparing bid vs. ask volume across updates.

If bid volume is increasing faster than ask volume → buyers gaining strength 📈

If ask volume is increasing faster than bid volume → sellers taking control 📉

🐋 3. Whale Activity Detection

Identifies large orders (buy/sell walls) that can move the market.

Threshold: Orders greater than 5 BTC.

Alerts when big buyers or sellers enter the market.

📈 4. Predictive Price Movement Analysis

Tracks bid/ask price trends over time to predict future movements.

If bids are rising and asks are falling, it signals a bullish trend.

If bids are falling and asks are rising, it signals a bearish trend.
