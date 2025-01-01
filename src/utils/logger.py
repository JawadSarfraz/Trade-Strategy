import logging

def setup_logger(name, log_file, level=logging.INFO):
    """Set up a logger with the specified name, log file, and log level."""
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Example usage:
# logger = setup_logger("mexc_logger", "data/logs/mexc_test.log")
# logger.info("Log message")
