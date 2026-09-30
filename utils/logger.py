import logging
import sys
from pathlib import Path

def get_logger(name: str = "Framework"):
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "automation.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_format = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

    return logger