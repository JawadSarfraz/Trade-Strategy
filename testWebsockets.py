import time
from src.exchanges.websockets import WebSocketManager

if __name__ == "__main__":
    trading_pair = "BTC/USDT"  # Changeable
    print(f"\nStarting WebSocket for {trading_pair}...")

    # Initialize WebSocket Manager for Spot and Futures separately
    ws_manager_spot = WebSocketManager(is_futures=False)
    ws_manager_futures = WebSocketManager(is_futures=True)

    # Start WebSockets for both Spot & Futures
    ws_manager_spot.start_all(trading_pair)
    ws_manager_futures.start_all(trading_pair)

    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[EXIT] WebSocket connections closed.")
