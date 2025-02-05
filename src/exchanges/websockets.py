import threading
import json
import websocket
import time
from src.trading.order_book_tracker import OrderBookTracker

class WebSocketManager:
    """Handles WebSocket connections for Binance & MEXC order books."""

    def __init__(self):
        self.order_book_tracker = OrderBookTracker()
        self.exchanges = {
            "binance": self.start_binance_ws,
            "mexc": self.start_mexc_ws
        }
        self.threads = []

    def start_binance_ws(self, trading_pair="BTC/USDT"):
        """Connect to Binance WebSocket for order book updates."""
        symbol = trading_pair.replace("/", "").lower()  # Convert BTC/USDT → btcusdt
        url = f"wss://stream.binance.com:9443/ws/{symbol}@depth"

        def on_message(ws, message):
            data = json.loads(message)
            self.order_book_tracker.update_order_book("binance", data)

        def on_error(ws, error):
            print(f"[Binance WS Error] {error}")

        def on_close(ws, close_status_code, close_msg):
            print("[Binance WS] Closed. Reconnecting...")
            time.sleep(5)
            self.start_binance_ws(trading_pair)  # Reconnect WebSocket

        ws = websocket.WebSocketApp(url, on_message=on_message, on_error=on_error, on_close=on_close)
        ws.run_forever()

    def start_mexc_ws(self, trading_pair="BTC/USDT"):
        """Connect to MEXC WebSocket for order book updates."""
        symbol = trading_pair.replace("/", "_")  # Convert BTC/USDT → BTC_USDT
        url = "wss://wbs.mexc.com/ws"

        def on_open(ws):
            """Send subscription message on connection open."""
            payload = {
                "method": "SUBSCRIPTION",
                "params": [f"spot@public.limit.depth.v3.api@{symbol}"],
                "id": 1
            }
            ws.send(json.dumps(payload))

        def on_message(ws, message):
            data = json.loads(message)
            if "data" in data:
                self.order_book_tracker.update_order_book("mexc", data["data"])

        def on_error(ws, error):
            print(f"[MEXC WS Error] {error}")

        def on_close(ws, close_status_code, close_msg):
            print("[MEXC WS] Closed. Reconnecting...")
            time.sleep(5)
            self.start_mexc_ws(trading_pair)  # Reconnect WebSocket

        ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
        ws.run_forever()

    def start_all(self, trading_pair="BTC/USDT"):
        """Start WebSockets for all exchanges in separate threads."""
        for exchange, func in self.exchanges.items():
            thread = threading.Thread(target=func, args=(trading_pair,))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)