from collections import deque

class OrderBookTracker:
    def __init__(self, max_history=100):
        """Initialize a rolling buffer for Binance order book updates."""
        self.order_books = {
            "binance": deque(maxlen=max_history)  # Rolling buffer for Binance
        }

    def update_order_book(self, exchange, data):
        """Update the rolling buffer with new Binance order book data."""
        if exchange == "binance" and "bids" in data and "asks" in data:
            snapshot = {
                "timestamp": data.get("E", None),  # Event timestamp
                "bids": data["bids"][:5],  # Store top 5 bids
                "asks": data["asks"][:5]  # Store top 5 asks
            }
            self.order_books[exchange].append(snapshot)  # Append to buffer
            print(f"[{exchange.upper()} Order Book Update] Rolling buffer size: {len(self.order_books[exchange])}")

    def get_latest_snapshot(self):
        """Retrieve the latest Binance order book snapshot."""
        if self.order_books["binance"]:
            return self.order_books["binance"][-1]
        return None
