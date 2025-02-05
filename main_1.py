# import sys
# import os
# import threading

# # Add the src directory to Python's module search path
# sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# # Import utilities and exchange classes
# from src.utils.credentials import load_credentials
# from src.exchanges.binance import BinanceExchange
# from src.exchanges.mexc import MEXCExchange

# def fetch_order_books(trading_pair, exchange_name, exchange, results):
#     """Fetch and analyze the order book from the specified exchange."""
#     try:
#         spot_order_book = exchange.fetch_order_book(trading_pair)
#         futures_order_book = exchange.fetch_futures_order_book(trading_pair)
#         results.update({f"{exchange_name}_spot_order_book": spot_order_book})
#         results.update({f"{exchange_name}_futures_order_book": futures_order_book})
#     except Exception as e:
#         print(f"Error fetching order book from {exchange_name}: {e}")

# def display_top_10(order_book, order_type):
#     """Display the top 10 orders based on volume."""
#     orders = order_book.get(order_type, [])
#     # Sort by volume in descending order
#     sorted_orders = sorted(orders, key=lambda x: -float(x[1]))
#     top_10 = sorted_orders[:10]
#     for price, volume in top_10:
#         print(f"Price: {price}, Volume: {volume:.2f}")

# if __name__ == "__main__":
#     # Specify the trading pair
#     trading_pair_input = input("Enter the trading pair (e.g., btc): ").strip().upper()
#     trading_pair = f"{trading_pair_input}/USDT"

#     # Load API credentials
#     credentials = load_credentials()

#     # Initialize exchanges dynamically
#     exchanges = {
#         "binance": BinanceExchange(credentials["binance"]["apiKey"], credentials["binance"]["secret"]),
#         "mexc": MEXCExchange(credentials["mexc"]["apiKey"], credentials["mexc"]["secret"]),
#     }

#     results = {}

#     # Create threads for each exchange
#     threads = []
#     for name, exchange in exchanges.items():
#         threads.append(threading.Thread(target=fetch_order_books, args=(trading_pair, name, exchange, results)))

#     # Start threads
#     for thread in threads:
#         thread.start()

#     # Wait for threads to complete
#     for thread in threads:
#         thread.join()

#     # Process and display results for each exchange
#     for name, exchange in exchanges.items():
#         print(f"\n--- {name.upper()} Spot Order Book ---")
#         spot_order_book = results.get(f"{name}_spot_order_book", {})
#         if spot_order_book:
#             print("\nTop 10 Buy Orders (Bids):")
#             display_top_10(spot_order_book, "bids")

#             print("\nTop 10 Sell Orders (Asks):")
#             display_top_10(spot_order_book, "asks")
#         else:
#             print("No Spot Order Book data available.")

#         print(f"\n--- {name.upper()} Futures Order Book ---")
#         futures_order_book = results.get(f"{name}_futures_order_book", {})
#         if futures_order_book:
#             print("\nTop 10 Buy Orders (Bids):")
#             display_top_10(futures_order_book, "bids")

#             print("\nTop 10 Sell Orders (Asks):")
#             display_top_10(futures_order_book, "asks")
#         else:
#             print("No Futures Order Book data available.")
import time
import threading
from src.exchanges.websockets import WebSocketManager
from src.trading.order_book_tracker import OrderBookTracker

def monitor_order_books(order_book_tracker):
    """
    Periodically print the latest order book summary.
    Detects large orders and prints key insights.
    """
    while True:
        time.sleep(10)  # Update every 10 seconds
        print("\n--- Live Order Book Update ---")
        
        for exchange in ["binance", "mexc"]:
            order_book = order_book_tracker.get_order_book(exchange)

            if order_book["bids"] and order_book["asks"]:
                top_bid = max(order_book["bids"], key=lambda x: float(x[0]))
                top_ask = min(order_book["asks"], key=lambda x: float(x[0]))
                spread = float(top_ask[0]) - float(top_bid[0])

                print(f"\n[{exchange.upper()}] Order Book Snapshot")
                print(f"Top Bid: {top_bid}")
                print(f"Top Ask: {top_ask}")
                print(f"Spread: {spread:.5f} USDT")

                detect_large_orders(order_book, exchange)
            else:
                print(f"[{exchange.upper()}] No recent order book data.")

def detect_large_orders(order_book, exchange):
    """
    Identify large buy and sell orders in the order book.
    """
    threshold = 50000  # Set large order threshold (modify as needed)
    
    large_bids = [bid for bid in order_book["bids"] if float(bid[1]) > threshold]
    large_asks = [ask for ask in order_book["asks"] if float(ask[1]) > threshold]

    if large_bids or large_asks:
        print(f"\n[ALERT] Large Orders Detected on {exchange.upper()}:")
        if large_bids:
            print("🔹 Large Buy Orders:")
            for bid in large_bids:
                print(f"  Price: {bid[0]}, Volume: {bid[1]}")
        if large_asks:
            print("🔻 Large Sell Orders:")
            for ask in large_asks:
                print(f"  Price: {ask[0]}, Volume: {ask[1]}")

if __name__ == "__main__":
    trading_pair = "BTC/USDT"

    # Start WebSockets for live order book tracking
    ws_manager = WebSocketManager()
    ws_manager.start_all(trading_pair)

    # Initialize Order Book Tracker
    order_book_tracker = OrderBookTracker()

    # Start monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_order_books, args=(order_book_tracker,))
    monitor_thread.daemon = True
    monitor_thread.start()

    # Keep the script running
    while True:
        time.sleep(1)
