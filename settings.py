import json
import os
import uuid
from pathlib import Path

import json5
from dotenv import load_dotenv

load_dotenv()

import logging

# Stayforge_version
__version__ = "1.0.0"
DEBUG = json.loads(os.getenv("DEBUG", "false").lower())
BASE_PATH = Path(__file__).parent

# Metadata

TITLE = "Stayforge API"
OPENAPI_URL = '/openapi.json'
FAVICON_URL = 'https://www.stayforge.io/wp-content/uploads/2024/12/cropped-site_icon-1-32x32.png'
REDOC_WITH_GOOGLE_FONTS = True

# etcd
ETCD_ENDPOINT = os.getenv("ETCD_ENDPOINT", "etcd://etcd:2379")


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


logger = getLogger('Stayforge')

if DEBUG:
    logger.setLevel(logging.DEBUG)
    logger.warning("DEBUG MODE ENABLED! DO NOT USE IN PRODUCTION.")

# Mongodb
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "stayforge")

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")

# API descriptions file dir
DOCS_API_DESCRIPTION = BASE_PATH / 'docs' / 'api_description'

# Default models source and namespace
DEFAULT_MODEL_SOURCE = os.getenv("DEFAULT_MODEL_MARKET", "https://market.stayforge.io/model")
DEFAULT_MODEL_NAMESPACE = os.getenv("DEFAULT_MODEL_NAMESPACE", "stayforge")

# Token
REFRESH_TOKEN_BYTES = os.getenv("REFRESH_TOKEN_BYTES", 64)
ACCESS_TOKEN_BYTES = os.getenv("ACCESS_TOKEN_BYTES", 32)
REFRESH_TOKEN_TTL = 60 * 60 * 24 * 30
ACCESS_TOKEN_TTL = 60 * 60 * 24

# Service Account & IAM Settings
SUPERUSER_ACCOUNT_NAME = os.getenv("SUPERUSER_ACCOUNT_NAME", "superuser@role.auth.stayforge.net")
SUPERUSER_ACCOUNT_SECRET = os.getenv("SUPERUSER_ACCOUNT_SECRET", uuid.uuid4().hex)
SUPERUSER_ACCOUNT_IAM = json5.loads(os.getenv("SUPERUSER_ACCOUNT_IAM", '["admin"]'))

# Order Types
ORDER_TYPE: dict = {

    'booked': {
        "description": "Create this order means that the room is booked. "
                       "If checkout_at is exceeded and there is no in-using state, it will automatically be converted to close."
    },
    'in-using': {"description": "Create this order means that the room is in-using. "
                                "If checkout_at is exceeded, it will automatically be converted to wait-for-maintain"
                 },
    'wait-for-maintain': {
        "description": "When the guest check-out, the order will automatically change to this state. "
                       "This state does not end automatically until the close order is created."
    },
    'under-maintenance': {
        "description": "If you need to close the room for some reason, create an Order for this state. "
                       "**It should be noted that even if you reach checkout_at, the room will not be automatically converted to close.**"
    },
    'close': {
        "description": "After creating other types of orders, you must create a close order to end the room's occupation."
    }
}
