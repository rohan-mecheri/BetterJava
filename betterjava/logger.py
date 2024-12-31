"""
logger.py - Handles logging for BetterJava.
"""

import logging

def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # standard log  format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger