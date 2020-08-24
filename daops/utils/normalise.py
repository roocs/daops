import collections

from daops.utils.core import open_dataset


def normalise(collection):
    print(f"[INFO] Working on datasets: {collection}")
    norm_collection = collections.OrderedDict()

    for col, file_paths in collection.items():

        ds = open_dataset(col, file_paths)
        norm_collection[col] = ds

    return norm_collection


class ResultSet(object):
    def __init__(self, inputs=None):
        self._results = collections.OrderedDict()
        self.metadata = {"inputs": inputs, "process": "something", "version": 0.1}
        self.file_paths = []

    def add(self, col, result):
        self._results[col] = result
        self.file_paths.append(result)
