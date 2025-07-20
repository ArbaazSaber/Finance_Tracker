import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name: str = "app", log_dir:str ="logs", level: str=logging.INFO ):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        os.makedirs(log_dir, exist_ok=True)

        file_handler = RotatingFileHandler(
            filename=os.path.join(log_dir, f"{name}.log"),
            maxBytes=1_000_000,
            backupCount=3
        )

        file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
        file_handler.setFormatter(file_formatter)

        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s | %(message)s')
        console_handler.setFormatter(console_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    return logger

logger = get_logger()
logger.info("Logger Started...")