import pandas as pd
import time
import matplotlib.pyplot as plt

class OrderBookAnalysis:
    """Analyzes order book data for trend detection."""

    def __init__(self, order_book_buffer=None):  # ✅ Accept order_book_buffer
        self.order_book_buffer = order_book_buffer  # Store buffer reference
        self.spread_history = []  # Store bid-ask spreads
        self.cvd_history = []  # Store cumulative volume delta


    def compute_bid_ask_spread(self, order_book):
        """Computes the bid-ask spread and logs it over time."""
        
        # ✅ Ensure `order_book` is a DataFrame
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

    def compute_cvd(self, order_book_buffer):
        """Computes Cumulative Volume Delta (CVD) using stored order book updates."""
        print("ASDSADADDSA")
        cvd = 0
        cvd_values = []

        for order_book in order_book_buffer:
            if isinstance(order_book, dict):
                order_book = pd.DataFrame({
                    "Bid Price": [b[0] for b in order_book.get("b", [])],  
                    "Bid Volume": [b[1] for b in order_book.get("b", [])],  
                    "Ask Price": [a[0] for a in order_book.get("a", [])],  
                    "Ask Volume": [a[1] for a in order_book.get("a", [])]  
                })

            if order_book.empty:
                continue  

            bid_volume = order_book["Bid Volume"].sum()
            ask_volume = order_book["Ask Volume"].sum()
            delta_v = bid_volume - ask_volume  
            cvd += delta_v  
            cvd_values.append(cvd)

        self.cvd_history = cvd_values
        print(f"[CVD] Latest CVD Value: {cvd}")
        return cvd

    def get_cvd_history(self):
        """Returns CVD history as a DataFrame."""
        return pd.DataFrame(self.cvd_history, columns=['CVD'])

    def plot_cvd(self):
        """Plots the CVD trend over time."""
        if not self.cvd_history:
            print("[WARNING] No CVD data available for plotting.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(self.cvd_history, label='Cumulative Volume Delta', color='blue')
        plt.xlabel("Time (Updates)")
        plt.ylabel("CVD Value")
        plt.title("Cumulative Volume Delta (CVD) Over Time")
        plt.legend()
        plt.grid()
        plt.show()

    def plot_bid_ask_spread(self):
        """Plots the bid-ask spread trend over time."""
        df = self.get_spread_history()
        if df.empty:
            print("[WARNING] No spread data available for plotting.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(df["Timestamp"], df["Spread"], label='Bid-Ask Spread', color='red')
        plt.xlabel("Timestamp")
        plt.ylabel("Spread")
        plt.title("Bid-Ask Spread Over Time")
        plt.legend()
        plt.grid()
        plt.show()
