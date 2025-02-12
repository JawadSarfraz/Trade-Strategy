import json
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

class CVDSmoothing:
    """Class to apply SMA & EMA smoothing to CVD and plot it."""

    def __init__(self, cvd_file="../../data/cvd_data.json", price_file="../../data/price_data.json", plot_dir="../../plots"):
        self.cvd_file = cvd_file
        self.price_file = price_file
        self.plot_dir = plot_dir
        self.cvd_data = []
        self.price_data = []

        os.makedirs(self.plot_dir, exist_ok=True)  # Ensure plot directory exists

    def load_data(self):
        """Loads CVD and price data from JSON files."""
        if os.path.exists(self.cvd_file):
            with open(self.cvd_file, "r") as f:
                self.cvd_data = json.load(f)

        if os.path.exists(self.price_file):
            with open(self.price_file, "r") as f:
                self.price_data = json.load(f)

    def process_data(self):
        """Converts loaded data into Pandas DataFrames and applies smoothing."""
        if not self.cvd_data or not self.price_data:
            print("[ERROR] No CVD or price data available for analysis.")
            return None, None

        cvd_df = pd.DataFrame(self.cvd_data)
        price_df = pd.DataFrame(self.price_data)

        cvd_df = cvd_df.sort_values(by="timestamp")
        price_df = price_df.sort_values(by="timestamp")

        # Apply SMA & EMA smoothing
        cvd_df["SMA_CVD"] = cvd_df["cvd"].rolling(window=10, min_periods=1).mean()
        cvd_df["EMA_CVD"] = cvd_df["cvd"].ewm(span=10, adjust=False).mean()

        return cvd_df, price_df

    def plot_cvd_with_smoothing(self, cvd_df, price_df):
        """Plots CVD with SMA & EMA smoothing and saves it."""
        if cvd_df is None or price_df is None:
            print("[WARNING] No data available for plotting.")
            return

        timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        fig, ax1 = plt.subplots(2, 1, figsize=(12, 8))

        # CVD with smoothing
        ax1[0].plot(cvd_df["timestamp"], cvd_df["cvd"], label="Raw CVD", color="blue", alpha=0.4)
        ax1[0].plot(cvd_df["timestamp"], cvd_df["SMA_CVD"], label="SMA CVD", color="green")
        ax1[0].plot(cvd_df["timestamp"], cvd_df["EMA_CVD"], label="EMA CVD", color="red")
        ax1[0].set_xlabel("Timestamp")
        ax1[0].set_ylabel("CVD")
        ax1[0].set_title("CVD Trend with Smoothing")
        ax1[0].legend()
        ax1[0].grid()

        # Price trend
        ax1[1].plot(price_df["timestamp"], price_df["price"], label="Price", color="black")
        ax1[1].set_xlabel("Timestamp")
        ax1[1].set_ylabel("Price (USD)")
        ax1[1].set_title("Price Trend Over Time")
        ax1[1].legend()
        ax1[1].grid()

        plt.tight_layout()

        plot_filename = f"{self.plot_dir}/cvd_smoothing_{timestamp_str}.png"
        plt.savefig(plot_filename)
        print(f"[INFO] Plot saved as {plot_filename}")

        plt.show()

    def run(self):
        """Runs the full analysis workflow."""
        self.load_data()
        cvd_df, price_df = self.process_data()

        if cvd_df is not None and price_df is not None:
            self.plot_cvd_with_smoothing(cvd_df, price_df)


if __name__ == "__main__":
    analysis = CVDSmoothing()
    analysis.run()
