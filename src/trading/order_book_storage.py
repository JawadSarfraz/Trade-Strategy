import json
import time

def save_order_book(order_book, exchange):
    """Saves the order book to a JSON file with a timestamp."""
    timestamp = int(time.time())  # Unix timestamp
    filename = f"data/historical/{exchange}_order_book_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(order_book, f, indent=4)
    
    print(f"[INFO] Order book saved: {filename}")
