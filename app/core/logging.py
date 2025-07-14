import logging
import sys
import os
from app.core.config import config


INFO_LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(message)s"
DEBUG_LOG_FORMAT = "%(asctime)s - [%(levelname)s] - (%(filename)s:%(lineno)d) - %(message)s"

# Create logger
logger = logging.getLogger("bot_logger")
logger.setLevel(config.LOG_LEVEL)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# Create logs directory
log_directory = config.LOGS_DIR
os.makedirs(log_directory, exist_ok=True)
file_handler = logging.FileHandler(f"{log_directory}/bot.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)

# Create formatter and add it to handlers
formatter = logging.Formatter(DEBUG_LOG_FORMAT if config.ENVIRONMENT == "development" else INFO_LOG_FORMAT)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Adding handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
