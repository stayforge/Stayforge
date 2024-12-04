import os

from dotenv import load_dotenv

load_dotenv()

import logging

# Stayforge_version
__version__ = "1.0.0"

# Metadata

TITLE = "Stayforge API"
OPENAPI_URL = '/openapi.json'
FAVICON_URL = 'https://www.stayforge.io/wp-content/uploads/2024/12/cropped-site_icon-1-32x32.png'
REDOC_WITH_GOOGLE_FONTS=True


# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)

logger.addHandler(console_handler)

# Mongodb
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "stayforge")
