import logging
import sys
from pathlib import Path
from typing import Optional


def create_rca_logger(log_level: int = logging.DEBUG, log_file: Optional[Path] = None) -> logging.Logger:
    """Create and return the parent "rca" logger, to configure logging to a file for an app

    Args:
        log_level: Logging level for the log file
        log_file: Path to the log file to use

    Returns:
        The parent "rca" logger
    """
    logger = logging.getLogger("rca")
    logger.setLevel(log_level)
    logger.propagate = False

    if log_file is not None:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(module_name: str) -> logging.Logger:
    """Use the module name (__name__) to create a child of the "rca" logger"""

    # When running apps the __name__ is __main__
    if module_name == "__main__":
        app_name = Path(sys.modules["__main__"].__file__).stem
        return logging.getLogger(f"rca.app.{app_name}")
    else:
        return logging.getLogger(module_name)
