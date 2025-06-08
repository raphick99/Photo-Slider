import sys

from loguru import logger


def setup_logging():
    # Remove all existing handlers
    logger.remove()
    
    # Add stdout handler with custom format
    logger.add(
        sys.stdout,
        format='{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message} | {extra}',
        level='INFO',
        backtrace=True,
        diagnose=True
    )