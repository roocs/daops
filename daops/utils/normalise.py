import collections
import os

from loguru import logger

from daops.utils.core import open_dataset


def normalise(collection, apply_fixes=True):
    """
    Takes file paths and opens and fixes the dataset they make up.

    :param collection: Ordered dictionary of ds ids and their related file paths.
    :param apply_fixes: Boolean. If True fixes will be applied to datasets if needed. Default is True.
    :return: An ordered dictionary of ds ids and their fixed xarray Dataset.
    """

    logger.info(f"Working on datasets: {collection}")
    norm_collection = collections.OrderedDict()

    for dset, file_paths in collection.items():
        ds = open_dataset(dset, file_paths, apply_fixes)
        norm_collection[dset] = ds

    return norm_collection


class ResultSet(object):
    """A class to hold the results from an operation e.g. subset"""

    def __init__(self, inputs=None):
        self._results = collections.OrderedDict()
        self.metadata = {"inputs": inputs, "process": "something", "version": 0.1}
        self.file_uris = []

    def add(self, dset, result):
        """
        Adds outputs to an ordered dictionary with the ds id as the key.
        If the output is a file path this is also added to the file_paths variable
        so a list of file paths can be accessed independently.
        """

        self._results[dset] = result

        for item in result:
            if isinstance(item, str) and (
                os.path.isfile(item) or item.startswith("https")
            ):
                self.file_uris.append(item)
