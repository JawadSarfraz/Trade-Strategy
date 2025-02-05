import json
from tabulate import tabulate

class OrderBookTracker:
    """Tracks and processes order book updates for multiple exchanges."""

    def __init__(self):
        self.order_books = {
            "binance": {"bids": [], "asks": []},
            "mexc": {"bids": [], "asks": []}
        }

    def update_order_book(self, exchange, data):
        """Processes and updates the order book for the given exchange."""
        try:
            if exchange == "binance":
                bids = data.get("b", [])[:10]  # Extract top 10 bids
                asks = data.get("a", [])[:10]  # Extract top 10 asks

            elif exchange == "mexc":
                # Extract MEXC bids/asks from WebSocket response
                print(data)
                exit()
                if "d" in data and isinstance(data["d"], dict):
                    bid_price = data["d"].get("b")
                    bid_volume = data["d"].get("B")
                    ask_price = data["d"].get("a")
                    ask_volume = data["d"].get("A")

                    if bid_price and bid_volume and ask_price and ask_volume:
                        bids = [[bid_price, bid_volume]]
                        asks = [[ask_price, ask_volume]]
                    else:
                        print(f"[MEXC Warning] Incomplete order book data received. Skipping update.")
                        return
                else:
                    print(f"[MEXC Error] Unexpected data format: {json.dumps(data, indent=2)}")
                    return


            # Convert prices and volumes to float and filter out zero-volume orders
            self.order_books[exchange]["bids"] = [
                (float(price), float(volume)) for price, volume in bids if float(volume) > 0
            ]
            self.order_books[exchange]["asks"] = [
                (float(price), float(volume)) for price, volume in asks if float(volume) > 0
            ]

            # Sort order book (Bids: Descending, Asks: Ascending)
            self.order_books[exchange]["bids"].sort(key=lambda x: -x[0])
            self.order_books[exchange]["asks"].sort(key=lambda x: x[0])

            self.display_order_book(exchange)

        except Exception as e:
            print(f"[ERROR] {exchange} Order Book Processing Error: {e}")

    def display_order_book(self, exchange):
        """Displays the formatted order book for an exchange."""
        print(f"\n--- {exchange.upper()} Order Book ---")
        table_data = []
        for i in range(max(len(self.order_books[exchange]["bids"]), len(self.order_books[exchange]["asks"]))):
            bid_price, bid_volume = self.order_books[exchange]["bids"][i] if i < len(self.order_books[exchange]["bids"]) else ("", "")
            ask_price, ask_volume = self.order_books[exchange]["asks"][i] if i < len(self.order_books[exchange]["asks"]) else ("", "")
            table_data.append([bid_price, bid_volume, ask_price, ask_volume])

        headers = ["Bid Price", "Bid Volume", "Ask Price", "Ask Volume"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
