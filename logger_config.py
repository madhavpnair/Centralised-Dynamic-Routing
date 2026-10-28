import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(level=logging.DEBUG):
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_dir / "routing.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[console_handler, file_handler],
        force=True,
    )

def end_logging():
    for handler in logging.getLogger().handlers:
        if isinstance(handler, RotatingFileHandler):
            handler.stream.write("---------------------------------------\n")
            handler.flush()