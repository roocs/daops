"""Dataset-Aware Operations."""

__author__ = """Elle Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2018-2025 United Kingdom Research and Innovation"
__version__ = "0.16.0"

from functools import lru_cache

from clisops import config
from loguru import logger


@lru_cache(maxsize=1)
def _config_cached():
    import daops

    # TODO: fix this code in clisops
    return config.reload_config(daops.__file__)


def config_():
    cfg = _config_cached()
    return cfg


from .utils.common import enable_logging as enable_logging  # noqa: E402

# Disable logging for daops and remove the logger that is instantiated on import
logger.disable("daops")
logger.remove()
