import collections

from daops.utils.core import open_dataset


def normalise(data_refs):
    print(f'[INFO] Working on data refs: {data_refs}')
    norm_dsets = collections.OrderedDict()

    for data_ref, file_paths in data_refs.items():

        xr_dset = open_dataset(data_ref, file_paths)
        norm_dsets[data_ref] = xr_dset

    return norm_dsets


class ResultSet(object):

    def __init__(self, inputs=None):
        self._results = collections.OrderedDict()
        self.metadata = {'inputs': inputs, 'process': 'something', 'version': 0.1}
        self.file_paths = []

    def add(self, data_ref, result):
        self._results[data_ref] = result
        self.file_paths.append(result)
