import json
import matplotlib.pyplot as plt
import os

CVD_FILE = "data/cvd_data.json"

def load_cvd_data():
    """Loads stored CVD values from JSON file."""
    if not os.path.exists(CVD_FILE):
        print("[ERROR] No CVD data found!")
        return []

    with open(CVD_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print("[ERROR] Invalid JSON format in CVD data.")
            return []

def plot_cvd():
    """Manually plots the CVD trend."""
    cvd_data = load_cvd_data()
    if not cvd_data:
        print("[WARNING] No CVD data available for plotting.")
        return

    timestamps = [entry["timestamp"] for entry in cvd_data]
    cvd_values = [entry["cvd"] for entry in cvd_data]
    
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cvd_values, label="CVD", color="blue")
    plt.xlabel("Timestamp")
    plt.ylabel("Cumulative Volume Delta (CVD)")
    plt.title("CVD Trend Over Time")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    plot_cvd()
