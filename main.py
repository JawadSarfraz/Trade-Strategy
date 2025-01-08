import sys
import os
import threading

# Add the src directory to Python's module search path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import utilities and MEXC exchange class
from src.utils.credentials import load_credentials
from src.exchanges.mexc import MEXCExchange

def fetch_spot_order_book(trading_pair, mexc):
    """Fetch the spot order book from MEXC."""
    try:
        return mexc.fetch_order_book(trading_pair)
    except Exception as e:
        print(f"Error fetching spot order book: {e}")
        return {"bids": [], "asks": []}

def fetch_futures_order_book(trading_pair, mexc):
    """Fetch the futures order book from MEXC."""
    try:
        return mexc.fetch_futures_order_book(trading_pair)
    except Exception as e:
        print(f"Error fetching futures order book: {e}")
        return {"bids": [], "asks": []}

if __name__ == "__main__":
    # Specify the trading pair (e.g., BTC/USDT)
    trading_pair = input("Enter the trading pair (e.g., BTC/USDT): ").strip()

    # Load API credentials
    credentials = load_credentials()

    # Initialize MEXC API for spot and futures
    mexc = MEXCExchange(credentials["mexc"]["apiKey"], credentials["mexc"]["secret"])

    # Results container
    results = {}

    # Threads for fetching spot and futures order books
    threads = [
        threading.Thread(target=lambda: results.update({"spot_order_book": fetch_spot_order_book(trading_pair, mexc)})),
        threading.Thread(target=lambda: results.update({"futures_order_book": fetch_futures_order_book(trading_pair, mexc)}))
    ]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Fetch results
    spot_order_book = results.get("spot_order_book", {})
    futures_order_book = results.get("futures_order_book", {})

    # Display Spot Order Book
    print("\n--- Spot Order Book (Buy Orders - Top 10) ---")
    for price, volume in sorted(spot_order_book.get("bids", []), key=lambda x: -float(x[0]))[:10]:
        print(f"Price: {price}, Volume: {volume}")

    print("\n--- Spot Order Book (Sell Orders - Top 10) ---")
    for price, volume in sorted(spot_order_book.get("asks", []), key=lambda x: float(x[0]))[:10]:
        print(f"Price: {price}, Volume: {volume}")

    # Display Futures Order Book
    print("\n--- Futures Order Book (Buy Orders - Top 10) ---")
    for bid in sorted(futures_order_book.get("bids", []), key=lambda x: -float(x[0]))[:10]:
        price, volume = bid[:2]  # Extract only price and volume
        print(f"Price: {price}, Volume: {volume}")

    print("\n--- Futures Order Book (Sell Orders - Top 10) ---")
    for ask in sorted(futures_order_book.get("asks", []), key=lambda x: float(x[0]))[:10]:
        price, volume = ask[:2]  # Extract only price and volume
        print(f"Price: {price}, Volume: {volume}")