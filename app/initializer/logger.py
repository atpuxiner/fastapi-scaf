import sys
from pathlib import Path

from loguru import logger
from loguru._logger import Logger  # noqa

LOG_CONSOLE_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} {level} {file}:{line} {message}"
LOG_FILE_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} {level} {file}:{line} {message}"
LOG_FILE_PREFIX = "app"
LOG_ROTATION = "00:00"
LOG_RETENTION = "15 days"


def init_logger(
        debug: bool,
        log_dir: str = None,
) -> Logger:
    logger.remove(None)
    _lever = "DEBUG" if debug else "INFO"
    logger.add(
        sys.stdout,
        format=LOG_CONSOLE_FORMAT,
        level=_lever,
    )
    if log_dir:
        _log_dir = Path(log_dir)
        logger.add(
            _log_dir.joinpath(f"{LOG_FILE_PREFIX}-access.log"),
            format=LOG_FILE_FORMAT,
            level=_lever,
            rotation=LOG_ROTATION,
            retention=LOG_RETENTION,
            encoding="utf-8"
        )
        logger.add(
            _log_dir.joinpath(f"{LOG_FILE_PREFIX}-error.log"),
            format=LOG_FILE_FORMAT,
            level="ERROR",
            rotation=LOG_ROTATION,
            retention=LOG_RETENTION,
            encoding="utf-8"
        )
    return logger
