import threading
import json
import websocket
import time
import requests

# WebSocket URLs
MEXC_SPOT_WS_URL = "wss://wbs.mexc.com/ws"
MEXC_FUTURES_WS_URL = "wss://contract.mexc.com/ws"
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/{symbol}@depth"

class WebSocketManager:
    """Handles WebSocket connections for Binance & MEXC order books."""

    def __init__(self, is_futures=False):
        self.is_futures = is_futures  # Toggle between spot and futures
        self.exchanges = {
            "binance": self.start_binance_ws,
            "mexc": self.start_mexc_ws
        }
        self.threads = []
    
    def start_binance_ws(self, trading_pair="BTC/USDT"):
        """Connect to Binance WebSocket for order book updates."""
        symbol = trading_pair.replace("/", "").lower()  # Convert BTC/USDT → btcusdt
        url = BINANCE_WS_URL.format(symbol=symbol)

        def on_message(ws, message):
            data = json.loads(message)
            if "b" in data and "a" in data:
                bids = data.get("b", [])[:5]  # Top 5 bids
                asks = data.get("a", [])[:5]  # Top 5 asks
                print(f"\n[Binance Order Book Update] \nBids: {bids}\nAsks: {asks}")

        def on_error(ws, error):
            print(f"[Binance WS Error] {error}")

        def on_close(ws, close_status_code, close_msg):
            print("[Binance WS] Closed. Reconnecting...")
            time.sleep(5)
            self.start_binance_ws(trading_pair)  # Reconnect

        ws = websocket.WebSocketApp(url, on_message=on_message, on_error=on_error, on_close=on_close)
        ws.run_forever()

    def start_mexc_ws(self, trading_pair="BTC/USDT"):
        """Connect to MEXC WebSocket for order book updates."""
        symbol = trading_pair.replace("/", "")  # Convert BTC/USDT → BTCUSDT (MEXC uses no underscore)
        url = MEXC_FUTURES_WS_URL if self.is_futures else MEXC_SPOT_WS_URL

        def on_open(ws):
            """Send correct subscription message."""
            payload = {
                "method": "SUBSCRIPTION",
                "params": [f"spot@public.bookTicker.v3.api@{symbol}"],  # FIXED Subscription Format
                "id": 1
            }
            ws.send(json.dumps(payload))
            print(f"[MEXC WS] Subscribed to {'Futures' if self.is_futures else 'Spot'} Order Book for {trading_pair}")

        def on_message(ws, message):
            data = json.loads(message)
            if "data" in data:
                bids = data["data"].get("bids", [])[:5]
                asks = data["data"].get("asks", [])[:5]
                print(f"\n[MEXC Order Book Update] \nBids: {bids}\nAsks: {asks}")
            else:
                print(f"[DEBUG] Raw WebSocket Message from MEXC: {data}")

        def on_error(ws, error):
            print(f"[MEXC WS Error] {error}")

        def on_close(ws, close_status_code, close_msg):
            print("[MEXC WS] Closed. Reconnecting...")
            time.sleep(5)
            self.start_mexc_ws(trading_pair)  # Reconnect

        ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
        ws.run_forever()

    def start_all(self, trading_pair="BTC/USDT"):
        """Start WebSockets for all exchanges in separate threads."""
        for exchange, func in self.exchanges.items():
            thread = threading.Thread(target=func, args=(trading_pair,))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
