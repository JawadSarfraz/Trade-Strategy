import pandas as pd
import time
import json
import os
import matplotlib.pyplot as plt

CVD_FILE = "data/cvd_data.json"  # Define JSON file path

class OrderBookAnalysis:
    """Analyzes order book data for trend detection."""

    def __init__(self, order_book_buffer=None):
        self.order_book_buffer = order_book_buffer
        self.spread_history = []  # Store bid-ask spreads
        self.cvd_history = self.load_cvd_history()  # Load stored CVD

    def compute_bid_ask_spread(self, order_book):
        """Computes the bid-ask spread and logs it over time."""
        
        if isinstance(order_book, dict):  
            order_book = pd.DataFrame({
                "Bid Price": [b[0] for b in order_book.get("b", [])],  
                "Bid Volume": [b[1] for b in order_book.get("b", [])],  
                "Ask Price": [a[0] for a in order_book.get("a", [])],  
                "Ask Volume": [a[1] for a in order_book.get("a", [])]  
            })

        if order_book.empty:
            print("[WARNING] Order book is empty. Cannot compute spread.")
            return None

        try:
            highest_bid = order_book["Bid Price"].iloc[0]  
            lowest_ask = order_book["Ask Price"].iloc[0]   
            spread = lowest_ask - highest_bid
            timestamp = time.time()
            self.spread_history.append((timestamp, spread))

            print(f"[SPREAD] Time: {timestamp}, Bid: {highest_bid}, Ask: {lowest_ask}, Spread: {spread}")
            return spread

        except (IndexError, ValueError, TypeError) as e:
            print(f"[ERROR] Failed to compute bid-ask spread: {e}")
            return None

    def get_spread_history(self):
        """Returns bid-ask spread history as a DataFrame."""
        return pd.DataFrame(self.spread_history, columns=['Timestamp', 'Spread'])

    def compute_cvd(self):
        """Computes Cumulative Volume Delta (CVD) and stores it in JSON."""
        print("[DEBUG] compute_cvd() is running...")

        if not self.order_book_buffer:
            print("[WARNING] No order book data available.")
            return None

        cvd = self.cvd_history[-1]["cvd"] if self.cvd_history else 0  # Start from last CVD
        cvd_values = []

        for order_book in self.order_book_buffer:
            bid_volume = order_book["Bid Volume"].sum()
            ask_volume = order_book["Ask Volume"].sum()
            delta_v = bid_volume - ask_volume  # Compute Volume Delta (ΔV)
            cvd += delta_v  # Accumulate ΔV to compute CVD
            cvd_values.append({"timestamp": time.time(), "cvd": cvd})

        self.cvd_history.extend(cvd_values)  # Store computed CVD history
        self.save_cvd_history()  # Save to JSON
        print(f"[CVD] Latest CVD Value: {cvd}")
        return cvd

    def get_cvd_history(self):
        """Returns CVD history as a DataFrame."""
        return pd.DataFrame(self.cvd_history)

    def save_cvd_history(self):
        """Saves CVD values to a JSON file."""
        try:
            with open(CVD_FILE, "w") as f:
                json.dump(self.cvd_history, f, indent=4)
            print("[INFO] CVD history saved to JSON.")
        except Exception as e:
            print(f"[ERROR] Failed to save CVD history: {e}")

    def load_cvd_history(self):
        """Loads previous CVD values from JSON if file exists."""
        if os.path.exists(CVD_FILE):
            try:
                with open(CVD_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[ERROR] Failed to load CVD history: {e}")
        return []

    def plot_cvd(self):
        """Plots the CVD trend over time."""
        if not self.cvd_history:
            print("[WARNING] No CVD data available for plotting.")
            return

        timestamps = [entry["timestamp"] for entry in self.cvd_history]
        cvd_values = [entry["cvd"] for entry in self.cvd_history]

        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, cvd_values, label='Cumulative Volume Delta', color='blue')
        plt.xlabel("Time (Timestamps)")
        plt.ylabel("CVD Value")
        plt.title("Cumulative Volume Delta (CVD) Over Time")
        plt.legend()
        plt.grid()
        plt.show()
