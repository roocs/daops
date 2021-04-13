import intake

from .base import Catalog
from .util import MAX_DATETIME
from .util import MIN_DATETIME
from .util import parse_time
from daops import CONFIG

# from intake.config import conf as intake_config


class IntakeCatalog(Catalog):
    def __init__(self, project, url=None):
        super(IntakeCatalog, self).__init__(project)
        self.url = url or CONFIG.get(f"project:{self.project}", {}).get(
            "intake_catalog_url"
        )
        self._cat = None
        self._store = {}
        # intake_config["cache_dir"] = "/tmp/inventory_cache"

    @property
    def catalog(self):
        if not self._cat:
            self._cat = intake.open_catalog(self.url)
        return self._cat

    def load(self):
        if self.project not in self._store:
            self._store[self.project] = self.catalog[self.project].read()
        return self._store[self.project]

    def _query(self, collection, time=None):
        df = self.load()
        start, end = parse_time(time)

        if not start:
            start = MIN_DATETIME
        if not end:
            end = MAX_DATETIME
        # workaround for NaN values when no time axis (fx datasets)
        sdf = df.fillna({"start_time": MIN_DATETIME, "end_time": MAX_DATETIME})

        # search
        result = sdf.loc[
            (sdf.ds_id.isin(collection))
            & (sdf.end_time >= start)
            & (sdf.start_time <= end)
        ]
        records = {}
        for _, row in result.iterrows():
            if row.ds_id not in records:
                records[row.ds_id] = []
            records[row.ds_id].append(row.path)
        return records