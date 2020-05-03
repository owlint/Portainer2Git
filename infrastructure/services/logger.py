import sys

from loguru import logger as logging

from settings import dev


_logger = None


def logger():  # noqa: D103
    global _logger
    if not _logger:
        _logger = logging
        _logger.remove(handler_id=0)
        _logger.add(
            "activity.log",
            rotation="10 MB",
            retention=2,
            compression="gz",
            level="DEBUG",
        )
        _logger.add(sys.stdout, level="DEBUG" if dev() else "INFO")
    return _logger
