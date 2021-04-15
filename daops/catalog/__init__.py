from roocs_utils.exceptions import InvalidCollection

from .db import DBCatalog
from .intake import IntakeCatalog
from daops import CONFIG


def get_catalog(project):
    if CONFIG[f"project:{project}"].get("use_catalog"):
        try:
            catalog = DBCatalog(project)
            return catalog
        except Exception:
            raise InvalidCollection()


__all__ = [
    "get_catalog",
    "IntakeCatalog",
    "DBCatalog",
]
