import pandas as pd
import collections

class OrderBookTracker:
    """Tracks Binance order book updates with a rolling buffer."""

    def __init__(self, max_size=100):
        self.max_size = max_size  # Store only last 100 updates
        self.order_book_buffer = collections.deque(maxlen=max_size)  # Rolling buffer

    def update_order_book(self, exchange, data):
        """Processes incoming WebSocket order book data."""
        try:
            if "b" not in data or "a" not in data:
                print(f"[WARNING] Missing bid/ask data in update: {data}")
                return  # Skip processing if bids/asks are missing

            bids = data.get("b", [])[:5]  # Top 5 bids
            asks = data.get("a", [])[:5]  # Top 5 asks

            if not bids or not asks:
                print(f"[WARNING] Empty bids or asks received: {data}")

            # Convert to structured format
            formatted_data = {
                "Bid Price": [float(b[0]) for b in bids] if bids else [],
                "Bid Volume": [float(b[1]) for b in bids] if bids else [],
                "Ask Price": [float(a[0]) for a in asks] if asks else [],
                "Ask Volume": [float(a[1]) for a in asks] if asks else [],
            }

            # Convert to DataFrame for better handling
            df = pd.DataFrame(formatted_data)

            # Store in rolling buffer
            self.order_book_buffer.append(df)

            print("\n--- BINANCE Order Book ---")
            print(df.to_string(index=False))

        except KeyError as e:
            print(f"[ERROR] Order Book Update Failed - Missing Key: {e}")
        except Exception as e:
            print(f"[ERROR] Order Book Update Failed: {e}")


    def get_order_book(self):
        """Return the latest order book snapshot."""
        if self.order_book_buffer:
            latest_df = self.order_book_buffer[-1]  # Return latest DataFrame snapshot
            order_book_dict = {
                "b": latest_df[["Bid Price", "Bid Volume"]].values.tolist(),  # Convert back to list of lists
                "a": latest_df[["Ask Price", "Ask Volume"]].values.tolist()
            }
            return order_book_dict
        else:
            return {"b": [], "a": []}  
    
    def display_order_book(self):
        """Print top 5 bid/ask orders in tabular format."""
        if not self.order_book_buffer:
            print("[WARNING] No valid order book data yet.")
            return
        
        latest_order_book = self.order_book_buffer[-1]  # Get latest snapshot
        print("\n--- BINANCE Order Book ---")
        print(latest_order_book.to_string(index=False))  # Print formatted DataFrame

    def detect_large_orders(self, threshold=5.0):
        """Detects large buy/sell walls (orders > threshold BTC)."""
        if not self.order_book_buffer:
            return

        latest_order_book = self.order_book_buffer[-1]

        large_bids = latest_order_book[latest_order_book["Bid Volume"] > threshold]
        large_asks = latest_order_book[latest_order_book["Ask Volume"] > threshold]

        if not large_bids.empty or not large_asks.empty:
            print("\n🚨 [ALERT] Large Orders Detected 🚨")
            if not large_bids.empty:
                print(f"🔵 Large Buy Orders:\n{large_bids.to_string(index=False)}")
            if not large_asks.empty:
                print(f"🔴 Large Sell Orders:\n{large_asks.to_string(index=False)}")

    def detect_order_flow_imbalance(self):
        """Analyzes bid-ask volume imbalance."""
        if len(self.order_book_buffer) < 2:
            return

        latest = self.order_book_buffer[-1]
        prev = self.order_book_buffer[-2]

        latest_bid_volume = latest["Bid Volume"].sum()
        latest_ask_volume = latest["Ask Volume"].sum()
        prev_bid_volume = prev["Bid Volume"].sum()
        prev_ask_volume = prev["Ask Volume"].sum()

        bid_change = latest_bid_volume - prev_bid_volume
        ask_change = latest_ask_volume - prev_ask_volume

        if bid_change > ask_change:
            print("\n📈 Buyers are getting stronger!")
        elif ask_change > bid_change:
            print("\n📉 Sellers are getting stronger!")
