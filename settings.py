import os

from dotenv import load_dotenv

load_dotenv()

import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)

# Add handlers to the logger
logger.addHandler(console_handler)

# Example usage:
logger.info("Logging is set up.")

# Mongodb
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "stayforge")
