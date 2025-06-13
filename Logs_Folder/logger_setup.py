# logger_setup.py
import logging
import sys

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set minimum level

    # Avoid duplicate handlers if already set up
    if not logger.handlers:
        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    return logger

#Save logs to file
fh = logging.FileHandler('app.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)