import os
import sys
import logging as std_logging

from loguru import logger as logging
from sentry_sdk import capture_exception, init
from sentry_sdk.integrations.logging import EventHandler

from settings import dev


_logger = None
init(os.getenv("SentryDN"), default_integrations=(not dev()))


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
        if not dev():
            handler = EventHandler()
            _logger.add(handler, level="ERROR", format="{name} - {message}")
    return _logger


def report_exception(exception: Exception) -> None:
    """Report an exception to sentry.

    Args:
        exception: the exception to be reported

    Effects:
        The exception is reported in sentry

    """
    assert isinstance(exception, Exception)

    if not dev():
        capture_exception(exception)


class InterceptHandler(std_logging.Handler):
    def emit(self, record):
        logger_opt = logger().opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())
