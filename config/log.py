import logging

# Configure the logger
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format of log messages
)

# Create a logger object
logger = logging.getLogger(__name__)
