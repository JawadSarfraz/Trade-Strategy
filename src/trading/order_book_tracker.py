from collections import deque
from tabulate import tabulate

class OrderBookTracker:
    """Tracks order book updates and maintains a rolling buffer for analysis."""

    def __init__(self, max_updates=100):
        self.order_books = {"binance": deque(maxlen=max_updates)}  # Store last 100 updates

    def update_order_book(self, exchange, data):
        """Update order book for a given exchange and maintain rolling history."""
        bids = [(float(price), float(amount)) for price, amount in data.get("b", [])[:5]]
        asks = [(float(price), float(amount)) for price, amount in data.get("a", [])[:5]]

        # Save latest order book snapshot
        self.order_books[exchange].append({"bids": bids, "asks": asks})

        # Print latest order book
        self.display_order_book(exchange, bids, asks)

    def display_order_book(self, exchange, bids, asks):
        """Format and print order book using tabulate."""
        print(f"\n--- {exchange.upper()} Order Book ---\n")

        table = []
        for i in range(max(len(bids), len(asks))):  # Show top 5 levels
            bid_price, bid_volume = bids[i] if i < len(bids) else ("-", "-")
            ask_price, ask_volume = asks[i] if i < len(asks) else ("-", "-")
            table.append([bid_price, bid_volume, ask_price, ask_volume])

        print(tabulate(table, headers=["Bid Price", "Bid Volume", "Ask Price", "Ask Volume"], tablefmt="grid"))
