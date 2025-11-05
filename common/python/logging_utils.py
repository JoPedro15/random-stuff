import logging
import sys

"""
Simple, reusable logging setup utility.

This function initializes and returns a configured logger that writes clean, formatted
messages to standard output (stdout). It ensures no duplicate handlers are added even
if called multiple times.

Usage example:
    from common.python.logging_utils import setup

    logger = setup(name="spotify.client")
    logger.info("Access token received.")
    logger.error("API call failed: %s", response.text)

Args:
    level (int): Logging level, e.g., logging.INFO or logging.DEBUG.
    name (str, optional): Optional logger name. Defaults to the root logger.

Returns:
    logging.Logger: Configured logger instance.
"""

def setup(level: int = logging.INFO, name: str = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        fmt = "%(levelname)s %(name)s | %(message)s"
        handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
