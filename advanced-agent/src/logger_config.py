import logging
import logging.config
import os
from pathlib import Path

def setup_logging(log_file_path='logs/app.log', log_level=logging.DEBUG):
    """Sets up logging configuration for the application."""
    # Create logs directory if it doesn't exist
    log_dir = Path(log_file_path).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Clear any existing handlers to avoid duplicates
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )

def get_logger(name):
    """Get a logger instance for the given name."""
    return logging.getLogger(name)

# Set up logging when this module is imported
setup_logging()

# Create a default logger instance that can be imported directly
logger = get_logger(__name__)

# You can also create a main application logger
app_logger = get_logger('advanced-agent')