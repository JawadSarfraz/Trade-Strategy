import sys
import os

# Add the src directory to Python's module search path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import utilities and exchange classes
from src.utils.credentials import load_credentials
from src.utils.logger import setup_logger
from src.exchanges.mexc import MEXCExchange

def test_mexc_api():
    """
    Test MEXC API connection by fetching account balance and order book data.
    """
    # Set up logging
    logger = setup_logger("mexc_logger", "data/logs/mexc_test.log")
    logger.info("Starting MEXC API Test...")

    # Load credentials
    try:
        credentials = load_credentials()
        logger.info("Loaded API credentials successfully.")
    except Exception as e:
        logger.error(f"Failed to load API credentials: {e}")
        return

    # Initialize MEXC API
    try:
        mexc = MEXCExchange(credentials["mexc"]["apiKey"], credentials["mexc"]["secret"])
        logger.info("Initialized MEXC Exchange API.")
    except Exception as e:
        logger.error(f"Failed to initialize MEXC API: {e}")
        return

    # Fetch account balance
    try:
        balance = mexc.exchange.fetch_balance()
        logger.info("Fetched account balance successfully.")
        print("Account Balance:")
        for currency, details in balance['total'].items():
            if details > 0:  # Only display non-zero balances
                print(f"{currency}: {details}")
                logger.info(f"{currency}: {details}")
    except Exception as e:
        logger.error(f"Error fetching account balance: {e}")

    # Fetch order book
    try:
        order_book = mexc.fetch_order_book("BTC/USDT")
        if order_book:
            logger.info("Fetched order book successfully.")
            print("MEXC Order Book (Top 5 Bids/Asks):")
            print("Bids:", order_book["bids"][:10])
            print("Asks:", order_book["asks"][:10])
            logger.info(f"Bids: {order_book['bids'][:5]}")
            logger.info(f"Asks: {order_book['asks'][:5]}")
        else:
            logger.warning("Order book fetch returned empty.")
    except Exception as e:
        logger.error(f"Error fetching order book: {e}")


if __name__ == "__main__":
    test_mexc_api()