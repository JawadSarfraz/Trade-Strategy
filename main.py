import sys
import os
import threading

# Add the src directory to Python's module search path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import utilities and exchange classes
from src.utils.credentials import load_credentials
from src.exchanges.binance import BinanceExchange
from src.exchanges.mexc import MEXCExchange

def fetch_order_books(trading_pair, exchange_name, exchange, results):
    """Fetch and analyze the order book from the specified exchange."""
    try:
        spot_order_book = exchange.fetch_order_book(trading_pair)
        futures_order_book = exchange.fetch_futures_order_book(trading_pair)
        results.update({f"{exchange_name}_spot_order_book": spot_order_book})
        results.update({f"{exchange_name}_futures_order_book": futures_order_book})
    except Exception as e:
        print(f"Error fetching order book from {exchange_name}: {e}")

def display_top_10(order_book, order_type):
    """Display the top 10 orders based on volume."""
    orders = order_book.get(order_type, [])
    # Sort by volume in descending order
    sorted_orders = sorted(orders, key=lambda x: -float(x[1]))
    top_10 = sorted_orders[:10]
    for price, volume in top_10:
        print(f"Price: {price}, Volume: {volume:.2f}")

if __name__ == "__main__":
    # Specify the trading pair
    trading_pair_input = input("Enter the trading pair (e.g., btc): ").strip().upper()
    trading_pair = f"{trading_pair_input}/USDT"

    # Load API credentials
    credentials = load_credentials()

    # Initialize exchanges dynamically
    exchanges = {
        "binance": BinanceExchange(credentials["binance"]["apiKey"], credentials["binance"]["secret"]),
        "mexc": MEXCExchange(credentials["mexc"]["apiKey"], credentials["mexc"]["secret"]),
    }

    results = {}

    # Create threads for each exchange
    threads = []
    for name, exchange in exchanges.items():
        threads.append(threading.Thread(target=fetch_order_books, args=(trading_pair, name, exchange, results)))

    # Start threads
    for thread in threads:
        thread.start()

    # Wait for threads to complete
    for thread in threads:
        thread.join()

    # Process and display results for each exchange
    for name, exchange in exchanges.items():
        print(f"\n--- {name.upper()} Spot Order Book ---")
        spot_order_book = results.get(f"{name}_spot_order_book", {})
        if spot_order_book:
            print("\nTop 10 Buy Orders (Bids):")
            display_top_10(spot_order_book, "bids")

            print("\nTop 10 Sell Orders (Asks):")
            display_top_10(spot_order_book, "asks")
        else:
            print("No Spot Order Book data available.")

        print(f"\n--- {name.upper()} Futures Order Book ---")
        futures_order_book = results.get(f"{name}_futures_order_book", {})
        if futures_order_book:
            print("\nTop 10 Buy Orders (Bids):")
            display_top_10(futures_order_book, "bids")

            print("\nTop 10 Sell Orders (Asks):")
            display_top_10(futures_order_book, "asks")
        else:
            print("No Futures Order Book data available.")
