import logging
import os

LOG_PATH = os.path.join(
    os.path.dirname(__file__), 'logs', 'webparser.log'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_handler = logging.FileHandler(LOG_PATH)
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)-10s %(levelname)-10s %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)
