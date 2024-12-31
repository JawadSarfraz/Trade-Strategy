import os

# Define the folder structure
folder_structure = {
    "configs": [],
    "data": ["logs", "historical"],
    "src": [
        "exchanges",
        "analysis",
        "trading",
        "utils"
    ],
    "tests": []
}

# Create the directories
def create_folder_structure(base_path, structure):
    for root, subdirs in structure.items():
        root_path = os.path.join(base_path, root)
        os.makedirs(root_path, exist_ok=True)
        for subdir in subdirs:
            os.makedirs(os.path.join(root_path, subdir), exist_ok=True)

# Generate files for essential components
def create_base_files(base_path):
    base_files = {
        "configs/credentials.json": "{}",
        "configs/settings.py": 'TRADING_PAIR = "BTC/USDT"\nLARGE_ORDER_THRESHOLD = 50\nSTOP_LOSS_BUFFER = 50\n',
        "requirements.txt": "ccxt\npandas\nnumpy\nmatplotlib\nplotly\n",
        "main.py": 'if __name__ == "__main__":\n    print("Trading bot initialized.")\n',
        "README.md": "# Trading Bot\n\nThis is a trading bot for multi-exchange analysis and MEXC futures trading.",
    }
    for file_path, content in base_files.items():
        full_path = os.path.join(base_path, file_path)
        with open(full_path, "w") as file:
            file.write(content)

# Base path (current directory)
base_path = os.getcwd()

# Execute the creation of directories and files
create_folder_structure(base_path, folder_structure)
create_base_files(base_path)

print(f"Folder structure created under {base_path}")
