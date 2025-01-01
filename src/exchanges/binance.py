import ccxt

class BinanceExchange:
    def __init__(self, api_key, secret):
        self.exchange = ccxt.binance({
            "apiKey": api_key,
            "secret": secret,
            "enableRateLimit": True,
        })

    def fetch_order_book(self, symbol):
        """Fetch order book for a given symbol."""
        try:
            return self.exchange.fetch_order_book(symbol)
        except Exception as e:
            print(f"Error fetching order book from Binance: {e}")
            return None
