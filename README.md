# Binance Order Book Analysis

This project collects, processes, and analyzes order book data from Binance using WebSockets. It calculates key metrics such as the **bid-ask spread** and **Cumulative Volume Delta (CVD)** to understand market liquidity and price movements.

---

## 📌 Features

- **Real-time Order Book Updates**: Fetches top 5 bid-ask levels continuously.
- **Bid-Ask Spread Calculation**: Measures market liquidity.
- **Cumulative Volume Delta (CVD)**: Tracks market buying/selling pressure.
- **Data Storage & Analysis**: Rolling buffer of 100 snapshots.

---

## 🚀 How It Works

### 1️⃣ **Order Book Tracking** (`OrderBookTracker.py`)

- Stores the last **100** snapshots of order book updates.
- Extracts **top 5 bid/ask levels** from the incoming data.
- Converts updates into a structured **Pandas DataFrame**.

### 2️⃣ **Bid-Ask Spread Analysis** (`order_book_analysis.py`)

- Computes **spread** = `lowest_ask - highest_bid`.
- Maintains a history of spread values.
- Helps in liquidity analysis.

### 3️⃣ **Cumulative Volume Delta (CVD)** (`order_book_analysis.py`)

- **Formula**: `CVD = Σ (Bid Volume - Ask Volume)`
- Aggregates volume deltas over time.
- **Stores CVD values in `cvd_data.json`** for further analysis.
- Indicates **buying vs. selling dominance** in the market.

### 4️⃣ **CVD Analysis & Plotting** (`cvd_analysis.py`)

- Reads **`cvd_data.json`** to visualize the CVD trend.
- **Manual execution required**: CVD is plotted separately after data collection.
- Helps analyze cumulative volume trends over time.

---

## 🛠 Setup & Installation

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Run WebSocket Listener

```bash
python main.py
```

---

## 📊 Example Output

```
--- BINANCE Order Book ---
Bid Price   Bid Volume   Ask Price   Ask Volume
96534.65     3.51244    96534.66    1.52619
96534.54     0.00008    96535.99    0.02952
96534.40     0.00011    96536.00    0.04726
...

[SPREAD] Time: 1738982878.2227101, Bid: 96534.65, Ask: 96534.66, Spread: 0.01
[DEBUG] Calling compute_cvd()...
[CVD] Latest CVD Value: 6.13638
```

---

## 🎯 Next Steps

- ✅ Store **CVD values** for historical analysis
- ✅ Use **CVD for trading signals** (buy/sell pressure)
- ✅ **Plot CVD trends** to visualize market dominance
- 🔜 Add Order Flow Imbalance Detection for deeper market insights
