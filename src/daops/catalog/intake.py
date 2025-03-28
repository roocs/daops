"""Utilities for working with Intake catalogs."""

import intake

from daops import config_

from .base import Catalog
from .util import MAX_DATETIME, MIN_DATETIME, parse_time


class IntakeCatalog(Catalog):
    """Intake catalog class."""

    def __init__(self, project, url=None):
        super().__init__(project)
        self.url = url or config_().get("catalog", None).get("intake_catalog_url", None)
        self._cat = None
        self._store = {}
        # intake_config["cache_dir"] = "/tmp/inventory_cache"

    @property
    def catalog(self):
        """Return the intake catalog."""
        if not self._cat:
            self._cat = intake.open_catalog(self.url)
        return self._cat

    def load(self):
        """Load the catalog."""
        if self.project not in self._store:
            self._store[self.project] = self.catalog[self.project].read()
        return self._store[self.project]

    def _query(self, collection, time=None, time_components=None):
        df = self.load()
        start, end = parse_time(time, time_components)

        # workaround for NaN values when no time axis (fx datasets)
        df = df.fillna({"start_time": MIN_DATETIME, "end_time": MAX_DATETIME})

        # needed when catalog created from catalog_maker instead of above - can remove above line eventually
        df = df.replace({"start_time": {"undefined": MIN_DATETIME}})
        df = df.replace({"end_time": {"undefined": MAX_DATETIME}})

        # search
        result = df.loc[
            (df.ds_id.isin(collection))
            & (df.end_time >= start)
            & (df.start_time <= end)
        ]
        records = {}
        for _, row in result.iterrows():
            if row.ds_id not in records:
                records[row.ds_id] = []
            records[row.ds_id].append(row.path)
        return records
