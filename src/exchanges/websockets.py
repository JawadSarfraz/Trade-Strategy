import threading
import json
import websocket
import time
from src.trading.order_book_tracker import OrderBookTracker
from src.trading.order_book_analysis import OrderBookAnalysis

# Binance WebSocket URL
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/{symbol}@depth"

class WebSocketManager:
    """Manages Binance WebSocket for order book updates."""

    def __init__(self):
        self.order_book_tracker = OrderBookTracker()
        self.order_book_analysis = OrderBookAnalysis(self.order_book_tracker.order_book_buffer)  # Pass buffer
        self.threads = []
        

    def start_binance_ws(self, trading_pair="BTC/USDT"):
        """Connects to Binance WebSocket and receives order book updates."""
        symbol = trading_pair.replace("/", "").lower()
        url = BINANCE_WS_URL.format(symbol=symbol)

        def on_message(ws, message):
            """Handles WebSocket messages."""
            data = json.loads(message)

            # Validate that bids ('b') and asks ('a') exist in the message
            if "b" in data and "a" in data:
                self.order_book_tracker.update_order_book("binance", data)
                
                # Compute bid-ask spread after updating the order book
                order_book = self.order_book_tracker.get_order_book()
                print(order_book)
                
                self.order_book_analysis.compute_bid_ask_spread(order_book)

                    # 🛠️ Compute CVD (New Addition)
                print("[DEBUG] Calling compute_cvd()...")  # Debug statement
                self.order_book_analysis.compute_cvd()

            else:
                print(f"[Binance WS Error] Missing bids/asks in message: {data}")

        def on_error(ws, error):
            print(f"[Binance WS Error] {error}")

        def on_close(ws, close_status_code, close_msg):
            print("[Binance WS] Closed. Reconnecting in 5 seconds...")
            ws.close()  # Ensure the WebSocket is fully closed before reconnecting
            time.sleep(5)
            self.start_binance_ws(trading_pair)  # Restart WebSocket

        ws = websocket.WebSocketApp(url, on_message=on_message, on_error=on_error, on_close=on_close)
        ws.run_forever()

    def start_all(self, trading_pair="BTC/USDT"):
        """Starts Binance WebSocket in a separate thread."""
        thread = threading.Thread(target=self.start_binance_ws, args=(trading_pair,))
        thread.daemon = True
        thread.start()
        self.threads.append(thread)
