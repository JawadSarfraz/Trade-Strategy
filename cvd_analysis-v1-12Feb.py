import json
import pandas as pd
import matplotlib.pyplot as plt
import os

class CVDAnalysis:
    """Class to analyze Cumulative Volume Delta (CVD) and price data with divergences."""

    def __init__(self, cvd_file="data/cvd_data.json", price_file="data/price_data.json"):
        self.cvd_file = cvd_file
        self.price_file = price_file
        self.cvd_data = []
        self.price_data = []

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

        # Merge both datasets on timestamps (inner join for common time points)
        merged_df = pd.merge_asof(cvd_df, price_df, on="timestamp")
        # Rename possible duplicate column names if they exist
        if "price_x" in merged_df.columns and "price_y" in merged_df.columns:
            merged_df.rename(columns={"price_x": "price"}, inplace=True)
        elif "price_y" in merged_df.columns:
            merged_df.rename(columns={"price_y": "price"}, inplace=True)
        elif "price_x" in merged_df.columns:
            merged_df.rename(columns={"price_x": "price"}, inplace=True)

        print("[DEBUG] Merged DataFrame Columns:", merged_df.columns)  # Debugging statement
        print("[DEBUG] First few rows:\n", merged_df.head())  # Check first rows to confirm column names

        return merged_df

    def detect_divergences(self, df):
        """Detects bullish and bearish divergences between CVD and Price."""
        bullish_divs = []
        bearish_divs = []

        for i in range(1, len(df)):
            prev_cvd, current_cvd = df["cvd"].iloc[i - 1], df["cvd"].iloc[i]
            prev_price, current_price = df["price"].iloc[i - 1], df["price"].iloc[i]

            # Bullish Divergence: CVD increasing, Price flat/decreasing
            if current_cvd > prev_cvd and current_price <= prev_price:
                bullish_divs.append(df.iloc[i])

            # Bearish Divergence: CVD decreasing, Price flat/increasing
            elif current_cvd < prev_cvd and current_price >= prev_price:
                bearish_divs.append(df.iloc[i])

        return pd.DataFrame(bullish_divs), pd.DataFrame(bearish_divs)

    def plot_cvd_and_price(self, df, bullish_divs, bearish_divs):
        """Plots CVD trends and Price trends with divergences highlighted."""
        if df is None:
            print("[WARNING] No data available for plotting.")
            return

        fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

        # CVD Plot
        ax[0].plot(df["timestamp"], df["cvd"], label="Raw CVD", color="lightblue")
        ax[0].plot(df["timestamp"], df["cvd"].rolling(10).mean(), label="SMA CVD", color="green")  # SMA smoothing
        ax[0].plot(df["timestamp"], df["cvd"].ewm(span=10, adjust=False).mean(), label="EMA CVD", color="red")  # EMA smoothing
        ax[0].set_ylabel("CVD")
        ax[0].set_title("CVD Trend with Smoothing")
        ax[0].legend()
        ax[0].grid()

        # Price Plot
        ax[1].plot(df["timestamp"], df["price"], label="Price", color="black")

        # Highlight divergences
        if not bullish_divs.empty:
            ax[1].scatter(bullish_divs["timestamp"], bullish_divs["price"], color="green", marker="o", label="Bullish Divergence", s=50)
        if not bearish_divs.empty:
            ax[1].scatter(bearish_divs["timestamp"], bearish_divs["price"], color="red", marker="o", label="Bearish Divergence", s=50)

        ax[1].set_ylabel("Price (USD)")
        ax[1].set_title("Price Trend Over Time with Divergences")
        ax[1].legend()
        ax[1].grid()

        plt.tight_layout()
        plt.savefig("plots/cvd_price_analysis.png")  # ✅ Save plot instead of just showing
        plt.show()

    def run_analysis(self):
        """Runs the full analysis workflow: Load data, process, and plot."""
        self.load_data()
        df = self.process_data()

        if df is not None:
            bullish_divs, bearish_divs = self.detect_divergences(df)
            self.plot_cvd_and_price(df, bullish_divs, bearish_divs)


if __name__ == "__main__":
    analysis = CVDAnalysis()
    analysis.run_analysis()