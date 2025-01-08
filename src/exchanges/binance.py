# import ccxt
# import requests

# class BinanceExchange:
#     def __init__(self, api_key, secret):
#         self.exchange = ccxt.binance({
#             "apiKey": api_key,
#             "secret": secret,
#             "enableRateLimit": True,
#         })

#     def fetch_order_book(self, symbol):
#         """Fetch the full order book for a given symbol."""
#         try:
#             # Fetch order book with the maximum available limit
#             return self.exchange.fetch_order_book(symbol, params={"limit": 500})
#         except Exception as e:
#             print(f"Error fetching order book from Binance: {e}")
#             return None


#     def fetch_order_book(self, symbol, depth=50):
#         """
#         Fetch spot order book for a given symbol with a specified depth.
#         :param symbol: Trading pair, e.g., BTC/USDT
#         :param depth: Number of levels to fetch (default: 50)
#         :return: Order book dictionary
#         """
#         try:
#             return self.exchange.fetch_order_book(symbol, params={"limit": depth})
#         except Exception as e:
#             print(f"Error fetching spot order book from Binance: {e}")
#             return None

#     def fetch_futures_order_book(self, symbol, limit=20):
#         """
#         Fetch the futures order book for a given symbol.
#         :param symbol: Trading pair, e.g., BTC_USDT
#         :param limit: Number of levels to fetch
#         :return: A dictionary with 'bids' and 'asks'
#         """
#         endpoint = f"{self.futures_base_url}/depth"
#         params = {"symbol": symbol.replace("/", ""), "limit": limit}

#         try:
#             response = requests.get(endpoint, params=params)
#             if response.status_code == 200:
#                 data = response.json()
#                 return {
#                     "bids": data.get("bids", []),
#                     "asks": data.get("asks", []),
#                 }
#             else:
#                 print(f"Failed to fetch futures order book: {response.status_code}, {response.text}")
#         except Exception as e:
#             print(f"Error fetching futures order book from Binance: {e}")
#         return {"bids": [], "asks": []}

#     def analyze_order_book(self, order_book):
#         """
#         Analyze the order book to count orders and aggregate volumes.
#         :param order_book: Dictionary with 'bids' and 'asks'.
#         :return: Summary of order counts and volumes.
#         """
#         total_bids_count = len(order_book.get("bids", []))
#         total_bids_volume = sum(float(bid[1]) for bid in order_book.get("bids", []))

#         total_asks_count = len(order_book.get("asks", []))
#         total_asks_volume = sum(float(ask[1]) for ask in order_book.get("asks", []))

#         return {
#             "bids_count": total_bids_count,
#             "bids_volume": total_bids_volume,
#             "asks_count": total_asks_count,
#             "asks_volume": total_asks_volume,
#         }

#     def place_order(self, symbol, order_type, side, amount, price):
#         """
#         Place an order on Binance.
#         :param symbol: Trading pair, e.g., BTC/USDT
#         :param order_type: Type of order ('limit' or 'market')
#         :param side: Order side ('buy' or 'sell')
#         :param amount: Order amount
#         :param price: Order price (ignored for market orders)
#         :return: Response from the exchange
#         """
#         try:
#             return self.exchange.create_order(
#                 symbol=symbol,
#                 type=order_type,  # 'limit' or 'market'
#                 side=side,        # 'buy' or 'sell'
#                 amount=amount,
#                 price=price if order_type == "limit" else None,
#             )
#         except Exception as e:
#             print(f"Error placing order on Binance: {e}")
#             return None


import ccxt

class BinanceExchange:
    def __init__(self, api_key, secret):
        self.exchange = ccxt.binance({
            "apiKey": api_key,
            "secret": secret,
            "enableRateLimit": True,
        })

    def fetch_order_book(self, symbol):
        """Fetch the full order book for a given symbol."""
        try:
            return self.exchange.fetch_order_book(symbol, params={"limit": 500})
        except Exception as e:
            print(f"Error fetching order book from Binance: {e}")
            return None
