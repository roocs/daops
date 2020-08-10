import collections

from daops.utils.core import open_dataset


def normalise(collection):
    print(f'[INFO] Working on datasets: {collection}')
    norm_collection = collections.OrderedDict()

    for data_ref, file_paths in collection.items():

        ds = open_dataset(data_ref, file_paths)
        norm_collection[data_ref] = ds

    return norm_collection


class ResultSet(object):

    def __init__(self, inputs=None):
        self._results = collections.OrderedDict()
        self.metadata = {'inputs': inputs, 'process': 'something', 'version': 0.1}
        self.file_paths = []

    def add(self, data_ref, result):
        self._results[data_ref] = result
        self.file_paths.append(result)
