import threading
import json
import websocket
import time
from src.trading.order_book_tracker import OrderBookTracker
from src.trading.order_book_analysis import OrderBookAnalysis

# Binance WebSocket URL
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/{symbol}@depth"

class WebSocketManager:
    """Manages Binance WebSocket for order book updates and CVD analysis."""

    def __init__(self):
        self.order_book_tracker = OrderBookTracker()
        self.order_book_analysis = OrderBookAnalysis(self.order_book_tracker.order_book_buffer)  # Pass buffer
        self.threads = []
        self.price_data = []  # Store real-time price movements

    def on_message(self, ws, message):
        """Handles incoming WebSocket messages."""
        try:
            data = json.loads(message)

            if "b" in data and "a" in data:
                self.order_book_tracker.update_order_book("binance", data)
                
                # ✅ Extract the lowest ask price (market price)
                latest_price = float(data["a"][0][0])  

                # Compute bid-ask spread
                order_book = self.order_book_tracker.get_order_book()
                self.order_book_analysis.compute_bid_ask_spread(order_book)
                
                # ✅ Compute CVD using latest price
                self.order_book_analysis.compute_cvd(latest_price)
                
                # Store price data
                self.price_data.append({"timestamp": time.time(), "price": latest_price})
                with open("data/price_data.json", "w") as f:
                    json.dump(self.price_data, f, indent=4)

                print(f"[INFO] Latest Price: {latest_price} | CVD Updated")
            
            else:
                print(f"[Binance WS Error] Missing bids/asks in message: {data}")

        except Exception as e:
            print(f"[ERROR] WebSocket message handling failed: {e}")

    def on_error(self, ws, error):
        """Handles WebSocket errors."""
        print(f"[Binance WS Error] {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """Handles WebSocket closure and reconnects."""
        print("[Binance WS] Closed. Reconnecting in 5 seconds...")
        ws.close()  # Ensure proper closure
        time.sleep(5)
        self.start_binance_ws()  # Restart WebSocket

    def start_binance_ws(self, trading_pair="BTC/USDT"):
        """Connects to Binance WebSocket and receives order book updates."""
        symbol = trading_pair.replace("/", "").lower()
        url = BINANCE_WS_URL.format(symbol=symbol)

        ws = websocket.WebSocketApp(
            url,
            on_message=self.on_message,   # ✅ Pass the class method
            on_error=self.on_error,
            on_close=self.on_close
        )
        ws.run_forever()

    def start_all(self, trading_pair="BTC/USDT"):
        """Starts WebSocket in a separate thread to keep it running."""
        thread = threading.Thread(target=self.start_binance_ws, args=(trading_pair,))
        thread.daemon = True
        thread.start()
        self.threads.append(thread)