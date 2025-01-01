# src/exchanges/mexc.py

import ccxt

class MEXCExchange:
    def __init__(self, api_key, secret):
        self.exchange = ccxt.mexc({
            "apiKey": api_key,
            "secret": secret,
            "enableRateLimit": True
        })

    def fetch_order_book(self, symbol):
        """Fetch order book for a given symbol."""
        try:
            return self.exchange.fetch_order_book(symbol)
        except Exception as e:
            print(f"Error fetching order book from MEXC: {e}")
            return None

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
