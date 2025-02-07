"""Dataset-Aware Operations."""

__author__ = """Elle Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2018-2025 United Kingdom Research and Innovation"
__version__ = "0.13.0"

from functools import lru_cache

from loguru import logger
from roocs_utils.config import get_config as _get_config

import daops

# CONFIG = _get_config(daops)


@lru_cache(maxsize=1)
def _config_cached():
    return _get_config(daops)


def config_():
    cfg = _config_cached()
    return cfg


from .utils.common import enable_logging  # noqa

# Disable logging for daops and remove the logger that is instantiated on import
logger.disable("daops")
logger.remove()
