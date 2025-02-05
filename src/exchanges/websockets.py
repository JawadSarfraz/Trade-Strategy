import threading
import json
import websocket
import time
from src.trading.order_book_tracker import OrderBookTracker

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/{symbol}@depth"

class WebSocketManager:
    """Handles WebSocket connection for Binance order book."""

    def __init__(self):
        self.order_book_tracker = OrderBookTracker()
        self.threads = []

    def start_binance_ws(self, trading_pair="BTC/USDT"):
        """Connect to Binance WebSocket for order book updates."""
        symbol = trading_pair.replace("/", "").lower()  # Convert BTC/USDT → btcusdt
        url = BINANCE_WS_URL.format(symbol=symbol)

        def on_message(ws, message):
            data = json.loads(message)
            if "bids" in data and "asks" in data:
                self.order_book_tracker.update_order_book("binance", data)

        def on_error(ws, error):
            print(f"[Binance WS Error] {error}")

        def on_close(ws, close_status_code, close_msg):
            print("[Binance WS] Closed. Reconnecting...")
            time.sleep(5)
            self.start_binance_ws(trading_pair)  # Reconnect WebSocket

        ws = websocket.WebSocketApp(url, on_message=on_message, on_error=on_error, on_close=on_close)
        ws.run_forever()

    def start_all(self, trading_pair="BTC/USDT"):
        """Start Binance WebSocket in a separate thread."""
        thread = threading.Thread(target=self.start_binance_ws, args=(trading_pair,))
        thread.daemon = True
        thread.start()
        self.threads.append(thread)
