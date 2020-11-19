import collections
import glob
import os

import xarray as xr
from roocs_utils.project_utils import get_project_base_dir
from roocs_utils.project_utils import get_project_name

from daops import CONFIG
from daops import logging
from daops.utils.core import _wrap_sequence

LOGGER = logging.getLogger(__file__)


def _consolidate_dset(dset):
    """
    Constructs the file path for the input dataset depending on the type of dataset that is passed in.

    :param dset: Dataset to process. Formats currently accepted are file paths, paths to directories containing netCDF
                 files or dataset identifiers (ds ids).
    :return: The file path for the input dataset.
    """
    if dset.startswith("https"):
        raise Exception("This format is not supported yet")
    elif os.path.isfile(dset) or dset.endswith(".nc"):
        return dset
    elif os.path.isdir(dset):
        return os.path.join(dset, "*.nc")
    elif dset.count(".") > 6:
        project = get_project_name(dset)
        base_dir = get_project_base_dir(project)
        return base_dir.rstrip("/") + "/" + dset.replace(".", "/") + "/*.nc"
    else:
        raise Exception(f"The format of {dset} is not known.")


def convert_to_ds_id(dset):
    """
    Converts the input dataset to a drs id form to use with the elasticsearch index.

    :param dset: Dataset to process. Formats currently accepted are file paths and paths to directories.
    :return: The ds id for the input dataset.
    """
    projects = [_.split(":")[1] for _ in CONFIG.keys() if _.startswith("project:")]
    if dset.startswith("https"):
        raise Exception("This format is not supported yet")
    elif os.path.isfile(dset) or dset.endswith(".nc"):
        dset = dset.split("/")
        i = max(loc for loc, val in enumerate(dset) if val.lower() in projects)
        ds_id = ".".join(dset[i:-1])
        return ds_id
    elif os.path.isdir(dset):
        dset = dset.split("/")
        i = max(loc for loc, val in enumerate(dset) if val.lower() in projects)
        ds_id = ".".join(dset[i:])
        return ds_id
    else:
        raise Exception(f"The format of {dset} is not known.")


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
        consolidated = _consolidate_dset(dset)

        # convert dset to ds_id to work with elasticsearch index
        if not dset.count(".") > 6:
            dset = convert_to_ds_id(dset)

        if "time" in kwargs:
            time = kwargs["time"].asdict()

            file_paths = glob.glob(consolidated)
            LOGGER.info(f"Testing {len(file_paths)} files in time range: ...")
            files_in_range = []

            ds = xr.open_mfdataset(file_paths, use_cftime=True)

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
                ds = xr.open_dataset(fpath)

                found_years = {int(_) for _ in ds.time.dt.year}

                if required_years.intersection(found_years):
                    files_in_range.append(fpath)

            LOGGER.info(f"Kept {len(files_in_range)} files")
            consolidated = files_in_range[:]
            if len(files_in_range) == 0:
                raise Exception(f"No files found in given time range for {dset}")

        filtered_refs[dset] = consolidated

    return filtered_refs
