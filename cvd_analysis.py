import json
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

class CVDAnalysis:
    """Class to analyze Cumulative Volume Delta (CVD) and price data."""

    def __init__(self, cvd_file="data/cvd_data.json", price_file="data/price_data.json", plot_dir="plots"):
        self.cvd_file = cvd_file
        self.price_file = price_file
        self.plot_dir = plot_dir  # Directory to save plots
        self.cvd_data = []
        self.price_data = []

        # Ensure plot directory exists
        os.makedirs(self.plot_dir, exist_ok=True)

    def load_data(self):
        """Loads CVD and price data from JSON files."""
        if os.path.exists(self.cvd_file):
            with open(self.cvd_file, "r") as f:
                self.cvd_data = json.load(f)

        if os.path.exists(self.price_file):
            with open(self.price_file, "r") as f:
                self.price_data = json.load(f)

    def process_data(self):
        """Converts loaded data into Pandas DataFrames for analysis."""
        if not self.cvd_data or not self.price_data:
            print("[ERROR] No CVD or price data available for analysis.")
            return None, None

        cvd_df = pd.DataFrame(self.cvd_data)
        price_df = pd.DataFrame(self.price_data)

        # Ensure timestamps are sorted
        cvd_df = cvd_df.sort_values(by="timestamp")
        price_df = price_df.sort_values(by="timestamp")

        return cvd_df, price_df

    def plot_cvd_and_price(self, cvd_df, price_df):
        """Plots CVD and price trends and saves them as images."""
        if cvd_df is None or price_df is None:
            print("[WARNING] No data available for plotting.")
            return

        timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Format timestamp for filename

        # Create figure and subplots
        fig, ax1 = plt.subplots(2, 1, figsize=(12, 8))

        # Plot CVD
        ax1[0].plot(cvd_df["timestamp"], cvd_df["cvd"], label="CVD", color="blue")
        ax1[0].set_xlabel("Timestamp")
        ax1[0].set_ylabel("CVD")
        ax1[0].set_title("CVD Trend Over Time")
        ax1[0].legend()
        ax1[0].grid()

        # Plot Price
        ax1[1].plot(price_df["timestamp"], price_df["price"], label="Price", color="red")
        ax1[1].set_xlabel("Timestamp")
        ax1[1].set_ylabel("Price (USD)")
        ax1[1].set_title("Price Trend Over Time")
        ax1[1].legend()
        ax1[1].grid()

        plt.tight_layout()

        # Save the plot
        plot_filename = f"{self.plot_dir}/cvd_vs_price_{timestamp_str}.png"
        plt.savefig(plot_filename)
        print(f"[INFO] Plot saved as {plot_filename}")

        # Show the plot
        plt.show()

    def run_analysis(self):
        """Runs the full analysis workflow: Load data, process, and plot."""
        self.load_data()
        cvd_df, price_df = self.process_data()

        if cvd_df is not None and price_df is not None:
            self.plot_cvd_and_price(cvd_df, price_df)


if __name__ == "__main__":
    analysis = CVDAnalysis()
    analysis.run_analysis()