import collections

from daops.utils.core import open_dataset


def normalise(ds_ids):
    print(f'[INFO] Working on datasets: {ds_ids}')
    norm_dsets = collections.OrderedDict()

    for ds_id, file_paths in ds_ids.items():

        xr_dset = open_dataset(ds_id, file_paths)
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
