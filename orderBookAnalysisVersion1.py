import pandas as pd
import time

class OrderBookAnalysis:
    """Analyzes order book data for trend detection."""
    
    def __init__(self):
        self.spread_history = []  # Store bid-ask spreads

    def compute_bid_ask_spread(self, order_book):
        """Computes the bid-ask spread and logs it over time."""

        print("ASDASDASASDDADSAA")
        print(f"[DEBUG] Received Order Book Type: {type(order_book)}")
        print(f"[DEBUG] Order Book Content:\n{order_book}")

        # Handle DataFrame case
        if isinstance(order_book, pd.DataFrame):
            if order_book.empty:
                print("[WARNING] Order book DataFrame is empty. Cannot compute spread.")
                return None

            highest_bid = order_book["Bid Price"].max()
            lowest_ask = order_book["Ask Price"].min()

        # Handle Dictionary case (direct WebSocket data)
        elif isinstance(order_book, dict):
            if "b" not in order_book or "a" not in order_book:
                print(f"[ERROR] Missing bid/ask data: {order_book}")
                return None

            bids = order_book["b"]
            asks = order_book["a"]

            if not bids or not asks:
                print(f"[ERROR] Empty bid/ask lists: {order_book}")
                return None

            highest_bid = float(bids[0][0])
            lowest_ask = float(asks[0][0])

        else:
            print(f"[ERROR] Unexpected data type: {type(order_book)}")
            return None

        spread = lowest_ask - highest_bid
        timestamp = time.time()

        self.spread_history.append((timestamp, spread))
        print(f"[SPREAD] Time: {timestamp}, Bid: {highest_bid}, Ask: {lowest_ask}, Spread: {spread}")

        return spread


    
    def get_spread_history(self):
        """Returns bid-ask spread history as a DataFrame."""
        return pd.DataFrame(self.spread_history, columns=['Timestamp', 'Spread'])
