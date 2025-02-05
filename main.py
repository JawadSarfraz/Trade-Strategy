import json
import threading
import websocket
import time

# Define order books storage
order_books = {
    "binance": {"bids": [], "asks": []},
    "mexc": {"bids": [], "asks": []}
}

# Set threshold for large orders (modify based on market conditions)
LARGE_ORDER_THRESHOLD = 0.1  # Example: 10 BTC

# Exchange WebSocket URLs
EXCHANGE_WS_URLS = {
    "binance": "wss://stream.binance.com:9443/ws/btcusdt@depth",
    "mexc": "wss://wbs.mexc.com/ws"
}


### 🔹 WebSocket Handlers
def on_message(exchange, ws, message):
    """Handles WebSocket messages, processes order book data."""
    global order_books

    try:
        print(f"\n[DEBUG] Raw WebSocket Message from {exchange}: {message}")  # Debugging

        data = json.loads(message)

        # Process Binance order book update
        if exchange == "binance":
            bids = data.get("bids", [])
            asks = data.get("asks", [])
        
        # Process MEXC order book update
        elif exchange == "mexc":
            bids = data.get("data", {}).get("bids", [])
            asks = data.get("data", {}).get("asks", [])
        
        else:
            print(f"[ERROR] Unknown exchange: {exchange}")
            return

        # Convert strings to floats and store
        order_books[exchange]["bids"] = [(float(price), float(volume)) for price, volume in bids if float(volume) > 0]
        order_books[exchange]["asks"] = [(float(price), float(volume)) for price, volume in asks if float(volume) > 0]

        # Sort order book (Descending for Bids, Ascending for Asks)
        order_books[exchange]["bids"].sort(key=lambda x: -x[0])
        order_books[exchange]["asks"].sort(key=lambda x: x[0])

        # Print Order Book for Debugging
        print(f"\n[DEBUG] {exchange.upper()} Order Book (Bids & Asks):")
        print("  Bids:", order_books[exchange]["bids"][:5])
        print("  Asks:", order_books[exchange]["asks"][:5])

        # Display order book update
        print(f"\n--- {exchange.upper()} Order Book Update ---")
        display_top_orders(exchange)

        # Debugging: Check Large Order Detection
        detect_large_orders(exchange)

    except Exception as e:
        print(f"[ERROR] {exchange} WebSocket message processing error: {e}")



def on_open(exchange, ws):
    """Handles WebSocket connection opening and sends subscription request."""
    print(f"[CONNECTED] {exchange.upper()} WebSocket")

    if exchange == "binance":
        payload = {
            "method": "SUBSCRIBE",
            "params": ["btcusdt@depth"],
            "id": 1
        }
        ws.send(json.dumps(payload))

    elif exchange == "mexc":
        payload = {
            "method": "sub.depth",
            "params": {
                "symbol": "BTC_USDT",
                "limit": 50
            }
        }
        ws.send(json.dumps(payload))


def on_error(exchange, ws, error):
    """Handles WebSocket errors."""
    print(f"[ERROR] {exchange.upper()} WebSocket Error: {error}")


def on_close(exchange, ws, close_status_code, close_msg):
    """Handles WebSocket closure and attempts reconnection."""
    print(f"[DISCONNECTED] {exchange.upper()} WebSocket. Reconnecting in 5 seconds...")
    time.sleep(5)
    start_websocket(exchange)


### 🔹 Utility Functions
def display_top_orders(exchange):
    """Prints the top 5 buy and sell orders."""
    print("Top 5 Buy Orders (Bids):")
    for price, volume in order_books[exchange]["bids"][:5]:
        print(f"  Price: {price}, Volume: {volume}")

    print("\nTop 5 Sell Orders (Asks):")
    for price, volume in order_books[exchange]["asks"][:5]:
        print(f"  Price: {price}, Volume: {volume}")
    print("-" * 40)


def detect_large_orders(exchange):
    """Detects large buy and sell orders."""
    large_bids = [bid for bid in order_books[exchange]["bids"] if bid[1] > LARGE_ORDER_THRESHOLD]
    large_asks = [ask for ask in order_books[exchange]["asks"] if ask[1] > LARGE_ORDER_THRESHOLD]

    if large_bids or large_asks:
        print(f"\n🚨 [ALERT] Large Orders Detected on {exchange.upper()} 🚨")

    if large_bids:
        print("  🔵 Large Buy Orders:")
        for price, volume in large_bids:
            print(f"    Price: {price}, Volume: {volume}")

    if large_asks:
        print("  🔴 Large Sell Orders:")
        for price, volume in large_asks:
            print(f"    Price: {price}, Volume: {volume}")


def start_websocket(exchange):
    """Starts WebSocket connection for a given exchange."""
    ws = websocket.WebSocketApp(
        EXCHANGE_WS_URLS[exchange],
        on_message=lambda ws, msg: on_message(exchange, ws, msg),
        on_open=lambda ws: on_open(exchange, ws),
        on_error=lambda ws, err: on_error(exchange, ws, err),
        on_close=lambda ws, code, msg: on_close(exchange, ws, code, msg)
    )
    ws.run_forever()


### 🔹 Main Execution
if __name__ == "__main__":
    trading_pair = "BTC/USDT"

    # Start WebSockets for all exchanges in separate threads
    threads = []
    for exchange in EXCHANGE_WS_URLS.keys():
        t = threading.Thread(target=start_websocket, args=(exchange,))
        t.start()
        threads.append(t)

    # Keep script running
    for t in threads:
        t.join()
