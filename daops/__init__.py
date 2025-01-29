"""Top-level package for daops.
daops - Dataset-Aware Operations"""

__author__ = """Elle Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD"
__version__ = "0.12.0"

from loguru import logger

from roocs_utils.config import get_config

import daops

CONFIG = get_config(daops)

from .utils.common import enable_logging  # noqa

# Disable logging for daops and remove the logger that is instantiated on import
logger.disable("daops")
logger.remove()
