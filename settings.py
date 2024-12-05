import os
import logging
import json

from dotenv import load_dotenv

load_dotenv()

import logging

# Stayforge_version
__version__ = "1.0.0"
DEBUG = json.loads(os.getenv("DEBUG", "false").lower())

# Metadata

TITLE = "Stayforge API"
OPENAPI_URL = '/openapi.json'
FAVICON_URL = 'https://www.stayforge.io/wp-content/uploads/2024/12/cropped-site_icon-1-32x32.png'
REDOC_WITH_GOOGLE_FONTS = True


def getLogger(name="stayforge"):
    l = logging.getLogger(name)
    l.setLevel(logging.INFO if DEBUG else logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Define color formats for different log levels
    formats = {
        logging.DEBUG: '\033[1;34m%(levelname)s:\033[0m\t\033[1;36m%(asctime)s\033[0m - \033[1;34m%(name)s\033[0m - %(message)s',
        # Blue
        logging.INFO: '\033[1;32m%(levelname)s:\033[0m\t\033[1;36m%(asctime)s\033[0m - \033[1;34m%(name)s\033[0m - %(message)s',
        # Green
        logging.WARNING: '\033[1;33m%(levelname)s:\033[0m\t\033[1;36m%(asctime)s\033[0m - \033[1;34m%(name)s\033[0m - %(message)s',
        # Yellow
        logging.ERROR: '\033[1;31m%(levelname)s:\033[0m\t\033[1;36m%(asctime)s\033[0m - \033[1;34m%(name)s\033[0m - %(message)s',
        # Red
        logging.CRITICAL: '\033[1;41m%(levelname)s:\033[0m\t\033[1;36m%(asctime)s\033[0m - \033[1;34m%(name)s\033[0m - %(message)s'
        # Red background
    }

    class ColoredFormatter(logging.Formatter):
        def format(self, record):
            log_fmt = formats.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)

    console_format = ColoredFormatter()
    console_handler.setFormatter(console_format)
    l.addHandler(console_handler)
    return l


logger = getLogger(__name__)

if DEBUG:
    logger.setLevel(logging.DEBUG)
    logger.warning("DEBUG MODE ENABLED! DO NOT USE IN PRODUCTION.")

# Mongodb
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "stayforge")
