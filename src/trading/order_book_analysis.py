import pandas as pd
import time

class OrderBookAnalysis:
    """Analyzes order book data for trend detection."""
    
    def __init__(self):
        self.spread_history = []  # Store bid-ask spread over time
    
    def compute_bid_ask_spread(self, order_book):
        """Computes the bid-ask spread and logs it over time."""
        if not order_book['bids'] or not order_book['asks']:
            print("[WARNING] Order book is empty. Cannot compute spread.")
            return None
        
        # Get highest bid and lowest ask
        highest_bid = order_book['bids'][0][0]  # Top bid price
        lowest_ask = order_book['asks'][0][0]   # Top ask price
        
        spread = lowest_ask - highest_bid
        timestamp = time.time()
        
        # Store spread history
        self.spread_history.append((timestamp, spread))
        
        print(f"[SPREAD] Time: {timestamp}, Bid: {highest_bid}, Ask: {lowest_ask}, Spread: {spread}")
        
        return spread
    
    def get_spread_history(self):
        """Returns bid-ask spread history as a DataFrame."""
        df = pd.DataFrame(self.spread_history, columns=['Timestamp', 'Spread'])
        return df
