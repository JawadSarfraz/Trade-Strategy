import ccxt
import requests
from src.exchanges.base_exchange import BaseExchange

class MEXCExchange(BaseExchange):
    def __init__(self, api_key, secret):
        self.exchange = ccxt.mexc({
            "apiKey": api_key,
            "secret": secret,
            "enableRateLimit": True
        })
        self.futures_base_url = "https://contract.mexc.com/api/v1"

    def fetch_order_book(self, symbol):
        """Fetch the full spot order book for a given symbol."""
        try:
            return self.exchange.fetch_order_book(symbol, params={"limit": 500})
        except Exception as e:
            print(f"Error fetching spot order book from MEXC: {e}")
            return {"bids": [], "asks": []}

    def fetch_futures_order_book(self, symbol):
        """Fetch the full futures order book for a given symbol."""
        endpoint = f"{self.futures_base_url}/contract/depth/{symbol.replace('/', '_')}"
        try:
            response = requests.get(endpoint, params={"limit": 500})  # Request all levels
            if response.status_code == 200:
                data = response.json()
                if "data" in data:
                    return {
                        "bids": [(float(bid[0]), float(bid[1])) for bid in data["data"]["bids"]],
                        "asks": [(float(ask[0]), float(ask[1])) for ask in data["data"]["asks"]],
                    }
            print(f"Unexpected response format: {response.text}")
        except Exception as e:
            print(f"Error fetching futures order book from MEXC: {e}")
        return {"bids": [], "asks": []}
