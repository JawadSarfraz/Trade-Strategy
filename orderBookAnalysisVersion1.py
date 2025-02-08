import pandas as pd
import time

class OrderBookAnalysis:
    """Analyzes order book data for trend detection."""
    
    def __init__(self):
        self.spread_history = []  # Store bid-ask spread over time
    
    def compute_bid_ask_spread(self, order_book):
        """Computes the bid-ask spread and logs it over time."""
        if not order_book or "b" not in order_book or "a" not in order_book:
            print("[WARNING] Invalid order book structure.")
            return None

        bids = order_book["b"]
        asks = order_book["a"]

        if not bids or not asks:
            print("[WARNING] Order book is empty. Cannot compute spread.")
            return None

        try:
            # Get highest bid and lowest ask
            highest_bid = float(bids[0][0])  # Top bid price
            lowest_ask = float(asks[0][0])   # Top ask price
            
            spread = lowest_ask - highest_bid
            timestamp = time.time()

            # Ensure spread history is initialized
            if not hasattr(self, "spread_history"):
                self.spread_history = []  # Initialize it if missing

            # Store spread history
            self.spread_history.append((timestamp, spread))
            
            print(f"[SPREAD] Time: {timestamp}, Bid: {highest_bid}, Ask: {lowest_ask}, Spread: {spread}")
            
            return spread

        except (IndexError, ValueError, TypeError) as e:
            print(f"[ERROR] Failed to compute bid-ask spread: {e}")
            return None
    
    def get_spread_history(self):
        """Returns bid-ask spread history as a DataFrame."""
        df = pd.DataFrame(self.spread_history, columns=['Timestamp', 'Spread'])
        return df
