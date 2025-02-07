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