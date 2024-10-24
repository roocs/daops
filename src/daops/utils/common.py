from typing import List

from clisops import enable_logging as _enable_logging
from loguru import logger


def _logging_examples() -> None:
    """Testing module"""
    logger.trace("0")
    logger.debug("1")
    logger.info("2")
    logger.success("2.5")
    logger.warning("3")
    logger.error("4")
    logger.critical("5")


def enable_logging() -> List[int]:
    logger.enable("daops")
    return _enable_logging()
