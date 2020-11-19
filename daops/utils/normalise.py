import collections
import os

from daops import logging
from daops.utils.core import open_dataset

LOGGER = logging.getLogger(__file__)


def normalise(collection):
    """
    Takes file paths and opens and fixes the dataset they make up.

    :param collection: Ordered dictionary of ds ids and their related file paths.
    :return: An ordered dictionary of ds ids and their fixed xarray Dataset.
    """

    LOGGER.info(f"Working on datasets: {collection}")
    norm_collection = collections.OrderedDict()

    for dset, file_paths in collection.items():

        ds = open_dataset(dset, file_paths)
        norm_collection[dset] = ds

    return norm_collection


class ResultSet(object):
    """ A class to hold the results from an operation e.g. subset """

    def __init__(self, inputs=None):
        self._results = collections.OrderedDict()
        self.metadata = {"inputs": inputs, "process": "something", "version": 0.1}
        self.file_paths = []

    def add(self, dset, result):
        """
        Adds outputs to an ordered dictionary with the ds id as the key.
        If the output is a file path this is also added to the file_paths variable
        so a list of file paths can be accessed independently.
        """

        self._results[dset] = result

        for item in result:
            if isinstance(item, str) and os.path.isfile(item):
                self.file_paths.append(item)
