import pandas as pd
import collections

class OrderBookTracker:
    """Tracks Binance order book updates with a rolling buffer."""

    def __init__(self, max_size=100):
        self.max_size = max_size  # Store only last 100 updates
        self.order_book_buffer = collections.deque(maxlen=max_size)  # Rolling buffer
        self.order_book = {
            "binance": {"bids": [], "asks": []}  # Ensure order book structure is initialized
        }

    def update_order_book(self, exchange, data):
        """Updates the order book with the latest data from Binance."""
        try:
            # Ensure 'b' (bids) and 'a' (asks) keys exist in the data
            if "b" in data and "a" in data:
                self.order_book[exchange]["bids"] = [(float(price), float(volume)) for price, volume in data["b"]]
                self.order_book[exchange]["asks"] = [(float(price), float(volume)) for price, volume in data["a"]]

                # Debugging: Verify if data is actually stored
                print(f"\n--- {exchange.upper()} Order Book ---")
                df = pd.DataFrame(self.order_book[exchange]["bids"][:5], columns=["Bid Price", "Bid Volume"])
                df["Ask Price"], df["Ask Volume"] = zip(*self.order_book[exchange]["asks"][:5])
                print(df.to_string(index=False))  # Pretty print order book
            else:
                print(f"[ERROR] Unexpected data format from {exchange}: {data}")

        except Exception as e:
            print(f"[ERROR] Order Book Update Failed: {e}")


    def display_order_book(self):
        """Print top 5 bid/ask orders in tabular format."""
        if not self.order_book_buffer:
            print("[WARNING] No valid order book data yet.")
            return
        
        latest_order_book = self.order_book_buffer[-1]
        bids = latest_order_book["bids"][:5]
        asks = latest_order_book["asks"][:5]

        df = pd.DataFrame({
            "Bid Price": [b[0] for b in bids],
            "Bid Volume": [b[1] for b in bids],
            "Ask Price": [a[0] for a in asks],
            "Ask Volume": [a[1] for a in asks]
        })

        print("\n--- BINANCE Order Book ---")
        print(df.to_string(index=False))

    def detect_large_orders(self, threshold=5.0):
        """Detects large buy/sell walls (orders > threshold BTC)."""
        if not self.order_book_buffer:
            return

        latest_order_book = self.order_book_buffer[-1]
        large_bids = [bid for bid in latest_order_book["bids"] if bid[1] > threshold]
        large_asks = [ask for ask in latest_order_book["asks"] if ask[1] > threshold]

        if large_bids or large_asks:
            print("\n🚨 [ALERT] Large Orders Detected 🚨")
            if large_bids:
                print(f"🔵 Large Buy Orders: {large_bids}")
            if large_asks:
                print(f"🔴 Large Sell Orders: {large_asks}")

    def detect_order_flow_imbalance(self):
        """Analyzes bid-ask volume imbalance."""
        if len(self.order_book_buffer) < 2:
            return

        latest = self.order_book_buffer[-1]
        prev = self.order_book_buffer[-2]

        latest_bid_volume = sum(b[1] for b in latest["bids"])
        latest_ask_volume = sum(a[1] for a in latest["asks"])
        prev_bid_volume = sum(b[1] for b in prev["bids"])
        prev_ask_volume = sum(a[1] for a in prev["asks"])

        bid_change = latest_bid_volume - prev_bid_volume
        ask_change = latest_ask_volume - prev_ask_volume

        if bid_change > ask_change:
            print("\n📈 Buyers are getting stronger!")
        elif ask_change > bid_change:
            print("\n📉 Sellers are getting stronger!")
