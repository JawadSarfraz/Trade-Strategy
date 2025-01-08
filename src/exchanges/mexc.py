import ccxt
import requests

class MEXCExchange:
    def __init__(self, api_key, secret):
        self.exchange = ccxt.mexc({
            "apiKey": api_key,
            "secret": secret,
            "enableRateLimit": True
        })
        self.futures_base_url = "https://contract.mexc.com/api/v1"  # MEXC Futures API Base URL

    def fetch_order_book(self, symbol):
        """Fetch spot order book for a given symbol."""
        try:
            return self.exchange.fetch_order_book(symbol)
        except Exception as e:
            print(f"Error fetching spot order book from MEXC: {e}")
            return None

    def fetch_futures_order_book(self, symbol, limit=10):
        """
        Fetch the futures order book for a given symbol.
        :param symbol: Trading pair, e.g., BTC_USDT
        :param limit: Number of levels to fetch
        :return: A dictionary with 'bids' and 'asks'
        """
        endpoint = f"{self.futures_base_url}/contract/depth/{symbol.replace('/', '_')}"
        params = {"limit": limit}

        try:
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                data = response.json()
                if "data" in data:
                    return {
                        "bids": data["data"]["bids"],
                        "asks": data["data"]["asks"],
                    }
                else:
                    print(f"Unexpected response format: {data}")
            else:
                print(f"Failed to fetch futures order book: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error fetching futures order book: {e}")
        return {"bids": [], "asks": []}

    def place_order(self, symbol, order_type, side, amount, price):
        """Place an order on MEXC."""
        try:
            return self.exchange.create_order(
                symbol=symbol,
                type=order_type,  # 'limit' or 'market'
                side=side,        # 'buy' or 'sell'
                amount=amount,
                price=price
            )
        except Exception as e:
            print(f"Error placing order on MEXC: {e}")
            return None
