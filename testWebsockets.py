import websocket
import json

def on_message(ws, message):
    print(f"[MESSAGE] {message}")

def on_open(ws):
    print("[CONNECTED] WebSocket is open")
    payload = {
        "method": "SUBSCRIBE",
        "params": ["btcusdt@depth"],
        "id": 1
    }
    ws.send(json.dumps(payload))

ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws",
                            on_message=on_message,
                            on_open=on_open)
ws.run_forever()
