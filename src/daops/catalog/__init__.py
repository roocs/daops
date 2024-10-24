"""Catalog module for the daops package."""

from roocs_utils.exceptions import InvalidCollection

from daops import CONFIG

from .intake import IntakeCatalog


def get_catalog(project):
    """Get the catalog object for the project."""
    if CONFIG[f"project:{project}"].get("use_catalog"):
        try:
            catalog = IntakeCatalog(project)
            return catalog
        except Exception as err:
            raise InvalidCollection() from err


__all__ = [
    "IntakeCatalog",
    "get_catalog",
]
