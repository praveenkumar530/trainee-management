import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logger():
    _logger = logging.getLogger("gym_logger")
    _logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    _logger.addHandler(file_handler)
    _logger.addHandler(console_handler)

    return _logger

logger = setup_logger()
