import threading

class OrderBookTracker:
    """Tracks real-time order book updates from WebSockets."""

    def __init__(self):
        self.order_books = {
            "binance": {"bids": [], "asks": []},
            "mexc": {"bids": [], "asks": []}
        }
        self.lock = threading.Lock()  # Ensure thread safety

    def update_order_book(self, exchange, data):
        """Update order book state with latest WebSocket data."""
        with self.lock:
            if exchange == "binance":
                self.order_books["binance"]["bids"] = data.get("b", [])
                self.order_books["binance"]["asks"] = data.get("a", [])
            elif exchange == "mexc":
                self.order_books["mexc"]["bids"] = data.get("bids", [])
                self.order_books["mexc"]["asks"] = data.get("asks", [])

    def get_order_book(self, exchange):
        """Retrieve latest order book for an exchange."""
        with self.lock:
            return self.order_books.get(exchange, {"bids": [], "asks": []})

    def print_summary(self):
        """Print a summary of current order book state."""
        with self.lock:
            for exchange, book in self.order_books.items():
                print(f"\n[{exchange.upper()}] Order Book Snapshot")
                print(f"Top 3 Bids: {book['bids'][:3]}")
                print(f"Top 3 Asks: {book['asks'][:3]}")
