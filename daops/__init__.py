# -*- coding: utf-8 -*-

"""Top-level package for daops.
daops - Dataset-Aware Operations"""

__author__ = """Elle Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD"
__version__ = "0.2.0"

from roocs_utils.config import get_config
# init logging?
import daops

CONFIG = get_config(daops)
