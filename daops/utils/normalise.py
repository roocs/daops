import collections
import os

from daops.utils.core import open_dataset


def normalise(collection):
    print(f"[INFO] Working on datasets: {collection}")
    norm_collection = collections.OrderedDict()

    for dset, file_paths in collection.items():

        ds = open_dataset(dset, file_paths)
        norm_collection[dset] = ds

    return norm_collection


class ResultSet(object):
    def __init__(self, inputs=None):
        self._results = collections.OrderedDict()
        self.metadata = {"inputs": inputs, "process": "something", "version": 0.1}
        self.file_paths = []

    def add(self, dset, result):
        # print(result)

        self._results[dset] = result

        for item in result:
            if isinstance(item, str) and os.path.isfile(item):
                self.file_paths.append(item)
