"""Base class for catalog."""

import os

from daops import config_


def make_list(value):
    """Make a list from a value."""
    if isinstance(value, list):
        val = value
    else:
        val = [value]
    return val


class Catalog:  # noqa: D101
    def __init__(self, project):  # noqa: D107
        self.project = project

    def _query(self, collection, time=None, time_components=None):
        raise NotImplementedError

    def search(self, collection, time=None, time_components=None):
        """Search the catalog for datasets."""
        cols = make_list(collection)
        records = self._query(cols, time, time_components)
        result = Result(self.project, records)
        return result


class Result:
    """Class to hold the results of a catalog search."""

    def __init__(self, project, records):
        """Parse the records.

        Records are an OrderedDict of dataset ids with a list of files: {'ds_id': [files]}.
        """
        self.base_dir = config_().get(f"project:{project}", {}).get("base_dir")
        self.base_url = config_().get(f"project:{project}", {}).get("data_node_root")
        self.records = records

    @property
    def matches(self):
        """Return number of matched records."""
        return len(self.records)

    def __len__(self):  # noqa: D105
        return self.matches

    def _records(self, prefix):
        new_records = {}
        for ds_id, fpaths in self.records.items():
            new_records[ds_id] = [os.path.join(prefix, fpath) for fpath in fpaths]
        return new_records

    def files(self):
        """Return matched records with file path."""
        return self._records(prefix=self.base_dir)

    def download_urls(self):
        """Return matched records with download URL."""
        return self._records(prefix=self.base_url)
