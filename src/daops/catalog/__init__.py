from daops import CONFIG
from roocs_utils.exceptions import InvalidCollection

from .intake import IntakeCatalog


def get_catalog(project):
    if CONFIG[f"project:{project}"].get("use_catalog"):
        try:
            catalog = IntakeCatalog(project)
            return catalog
        except Exception:
            raise InvalidCollection()


__all__ = [
    "get_catalog",
    "IntakeCatalog",
]
