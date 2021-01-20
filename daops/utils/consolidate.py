import collections
import glob
import os

import xarray as xr
from roocs_utils.project_utils import dset_to_filepaths
from roocs_utils.project_utils import get_project_base_dir
from roocs_utils.project_utils import get_project_name
from roocs_utils.xarray_utils.xarray_utils import open_xr_dataset

from daops import logging
from daops.utils.core import _wrap_sequence

LOGGER = logging.getLogger(__file__)


def consolidate(collection, **kwargs):
    """
    Finds the file paths relating to each input dataset. If a time range has been supplied then only the files
    relating to this time range are recorded.

    :param collection: (roocs_utils.CollectionParameter) The collection of datasets to process.
    :param kwargs: Arguments of the operation taking place e.g. subset, average, or re-grid.
    :return: An ordered dictionary of each dataset from the collection argument and the file paths
             relating to it.
    """
    collection = _wrap_sequence(collection.tuple)

    filtered_refs = collections.OrderedDict()

    for dset in collection:
        consolidated = dset_to_filepaths(dset, force=True)

        if "time" in kwargs:
            try:
                time = kwargs["time"].asdict()

                file_paths = consolidated
                LOGGER.info(f"Testing {len(file_paths)} files in time range: ...")
                files_in_range = []

                ds = open_xr_dataset(dset)

                if time["start_time"] is None:
                    time["start_time"] = ds.time.values.min().strftime("%Y")
                if time["end_time"] is None:
                    time["end_time"] = ds.time.values.max().strftime("%Y")

                times = [
                    int(time["start_time"].split("-")[0]),
                    int(time["end_time"].split("-")[0]) + 1,
                ]
                required_years = set(range(*[_ for _ in times]))

                for i, fpath in enumerate(file_paths):

                    LOGGER.info(f"File {i}: {fpath}")

                    ds = open_xr_dataset(fpath)

                    found_years = {int(_) for _ in ds.time.dt.year}

                    if required_years.intersection(found_years):
                        files_in_range.append(fpath)

                LOGGER.info(f"Kept {len(files_in_range)} files")
                consolidated = files_in_range[:]
                if len(files_in_range) == 0:
                    raise Exception(f"No files found in given time range for {dset}")

            # catch where "time" attribute cannot be accessed in ds
            except AttributeError:
                pass

        filtered_refs[dset] = consolidated

    return filtered_refs
