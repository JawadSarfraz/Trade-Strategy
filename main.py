import time
from src.exchanges.websockets import WebSocketManager

if __name__ == "__main__":
    trading_pair = "BTC/USDT"

    print(f"\nStarting WebSocket for {trading_pair}...")
    ws_manager = WebSocketManager()
    ws_manager.start_all(trading_pair)

    while True:
        time.sleep(10)  # Keeps the script running
        