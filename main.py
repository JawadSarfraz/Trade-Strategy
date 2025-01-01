import sys
import os

# Add the src directory to Python's module search path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import utilities and exchange classes
from src.utils.credentials import load_credentials
from src.exchanges.mexc import MEXCExchange
from src.exchanges.binance import BinanceExchange

def fetch_aggregated_order_books(trading_pair):
    """Fetch and aggregate order books from multiple exchanges."""
    # Load API credentials
    credentials = load_credentials()

    # Initialize exchanges
    mexc = MEXCExchange(credentials["mexc"]["apiKey"], credentials["mexc"]["secret"])
    binance = BinanceExchange(credentials["binance"]["apiKey"], credentials["binance"]["secret"])

    # Fetch order books
    exchanges = {"MEXC": mexc}
    aggregated_bids = []
    aggregated_asks = []

    for name, exchange in exchanges.items():
        order_book = exchange.fetch_order_book(trading_pair)
        if order_book:
            print(f"Fetched order book from {name}")
            aggregated_bids += order_book["bids"]
            aggregated_asks += order_book["asks"]
        else:
            print(f"Failed to fetch order book from {name}")

    return aggregated_bids, aggregated_asks

if __name__ == "__main__":
    # Specify the trading pair (e.g., BTC/USDT)
    trading_pair = input("Enter the trading pair (e.g., BTC/USDT): ").strip()
    aggregated_bids, aggregated_asks = fetch_aggregated_order_books(trading_pair)

    # Display aggregated results
    print("\nAggregated Bids (Top 10):")
    for price, volume in sorted(aggregated_bids, key=lambda x: -x[0])[:10]:
        print(f"Price: {price}, Volume: {volume}")

    print("\nAggregated Asks (Top 10):")
    for price, volume in sorted(aggregated_asks, key=lambda x: x[0])[:10]:
        print(f"Price: {price}, Volume: {volume}")
