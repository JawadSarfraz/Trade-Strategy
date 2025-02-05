class OrderBookAnalysis:
    """Provides real-time analysis of the order book."""

    def __init__(self, tracker):
        self.tracker = tracker

    def detect_large_orders(self, exchange, threshold=10):
        """Identifies large buy/sell orders in the order book."""
        bids = self.tracker.order_books[exchange]["bids"]
        asks = self.tracker.order_books[exchange]["asks"]

        large_bids = [bid for bid in bids if bid[1] >= threshold]
        large_asks = [ask for ask in asks if ask[1] >= threshold]

        if large_bids or large_asks:
            print(f"\n🚨 [ALERT] Large Orders Detected on {exchange.upper()} 🚨")

        if large_bids:
            print("🔵 Large Buy Orders:")
            for price, volume in large_bids:
                print(f"  Price: {price}, Volume: {volume}")

        if large_asks:
            print("🔴 Large Sell Orders:")
            for price, volume in large_asks:
                print(f"  Price: {price}, Volume: {volume}")
