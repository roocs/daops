import collections

import xarray as xr

from daops import logging
from daops.utils import fixer

LOGGER = logging.getLogger(__file__)


def _wrap_sequence(obj):
    if isinstance(obj, str):
        obj = [obj]
    return obj


def is_dataref_characterised(dset):
    return True


def is_characterised(collection, require_all=False):
    """
    Takes in a collection (an individual data reference or a sequence of them).
    Returns an ordered dictionary of a collection of ids with a boolean value
    for each stating whether the dataset has been characterised.

    If `require_all` is True: return a single Boolean value.

    :param collection: one or more data references
    :param require_all: Boolean to require that all must be characterised
    :return: Ordered Dictionary OR Boolean (if `require_all` is True)
    """
    collection = _wrap_sequence(collection)
    resp = collections.OrderedDict()

    for dset in collection:
        _is_char = is_dataref_characterised(dset)

        if require_all and not _is_char:
            return False

        resp[dset] = is_dataref_characterised(dset)

    return resp


def open_dataset(ds_id, file_paths):
    """
    Opens an xarray Dataset and applies fixes if required.
    Fixes are applied to the data either before or after the dataset is opened.
    Whether a fix is a 'pre-processor' or 'post-processor' is defined in the
    fix itself.

    :param ds_id: Dataset identifier in the form of a drs id
                  e.g. cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga
    :param file_paths: (list) The file paths corresponding to the ds id.
    :return: xarray Dataset with fixes applied to the data.
    """

    fix = fixer.Fixer(ds_id)
    if fix.pre_processor:
        for pre_process in fix.pre_processors:
            LOGGER.info(f"Loading data with pre_processor: {pre_process.__name__}")
    else:
        LOGGER.info(f"Loading data")

    ds = xr.open_mfdataset(
        file_paths, preprocess=fix.pre_processor, use_cftime=True, combine="by_coords"
    )

    if fix.post_processors:
        for post_process in fix.post_processors:
            func, operands = post_process
            LOGGER.info(f"Running post-processing function: {func.__name__}")
            ds = func(ds, **operands)

    return ds
