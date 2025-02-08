import os
import sys
from pathlib import Path

from loguru import logger
from loguru._logger import Logger  # noqa

LOG_CONSOLE_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} {level} {file}:{line} {message}"
LOG_FILE_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} {level} {file}:{line} {message}"
LOG_FILE_PREFIX = "app"
LOG_ROTATION = "100 MB"
LOG_RETENTION = "15 days"
LOG_COMPRESSION = None
LOG_ENQUEUE = True
LOG_BACKTRACE = False
LOG_DIAGNOSE = False
LOG_PID = False


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
        enqueue=LOG_ENQUEUE,
        backtrace=LOG_BACKTRACE,
        diagnose=LOG_DIAGNOSE,
    )
    if log_dir:
        _log_dir = Path(log_dir)
        _log_access_file = _log_dir.joinpath(f"{LOG_FILE_PREFIX}-access.log")
        _log_error_file = _log_dir.joinpath(f"{LOG_FILE_PREFIX}-error.log")
        if LOG_PID:
            _log_access_file = str(_log_access_file).replace(".log", f".{os.getpid()}.log")
            _log_error_file = str(_log_error_file).replace(".log", f".{os.getpid()}.log")
        logger.add(
            _log_access_file,
            encoding="utf-8",
            format=LOG_FILE_FORMAT,
            level=_lever,
            rotation=LOG_ROTATION,
            retention=LOG_RETENTION,
            compression=LOG_COMPRESSION,
            enqueue=LOG_ENQUEUE,
            backtrace=LOG_BACKTRACE,
            diagnose=LOG_DIAGNOSE,
        )
        logger.add(
            _log_error_file,
            encoding="utf-8",
            format=LOG_FILE_FORMAT,
            level="ERROR",
            rotation=LOG_ROTATION,
            retention=LOG_RETENTION,
            compression=LOG_COMPRESSION,
            enqueue=LOG_ENQUEUE,
            backtrace=LOG_BACKTRACE,
            diagnose=LOG_DIAGNOSE,
        )
    return logger
