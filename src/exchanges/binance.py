import ccxt
from src.exchanges.base_exchange import BaseExchange

class BinanceExchange(BaseExchange):
    def __init__(self, api_key, secret):
        self.exchange = ccxt.binance({
            "apiKey": api_key,
            "secret": secret,
            "enableRateLimit": True,
        })

    def fetch_order_book(self, symbol):
        """Fetch the full spot order book for a given symbol."""
        try:
            return self.exchange.fetch_order_book(symbol, params={"limit": 500})
        except Exception as e:
            print(f"Error fetching order book from Binance: {e}")
            return {"bids": [], "asks": []}

    def fetch_futures_order_book(self, symbol):
        """Binance does not provide futures in this implementation."""
        return {"bids": [], "asks": []}
