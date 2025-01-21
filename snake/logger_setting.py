import logging
import colorlog

def logger_settings() -> None:
    logger = logging.getLogger("snake")
    color_fmt = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s][%(levelname)s] %(message)s",
        log_colors={
            "DEBUG": "yellow",
            "INFO": "green",
            "WARNING": "purple",
            "ERROR": "red",
            "CRITICAL": "red",
            })
    color_handler = colorlog.StreamHandler()
    color_handler.setFormatter(color_fmt)
    logger.addHandler(color_handler)