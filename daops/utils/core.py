import collections
import xarray as xr

from daops.utils import fixer

from daops import logging

LOGGER = logging.getLogger(__file__)


def _wrap_sequence(obj):
    if isinstance(obj, str):
        obj = [obj]
    return obj


def is_dataref_characterised(dset):
    return True


def is_characterised(collection, require_all=False):
    """
    Takes in an individual data reference or a sequence of them.
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
    # Wrap xarray open with required args

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


# Don't need - use pydoc locate
# def resolve_import(import_path):
#     """
#     Deconstructs path, imports module and returns callable.
#
#     :param import path: module and function as 'x.y.func' (of any depth)
#     :return: callable.
#     """
#     # Split last item off path
#     parts = import_path.split('.')
#     ipath = '.'.join(parts[:-1])
#     func_name = parts[-1]
#
#     # Import module then send the args and kwargs to the function
#     try:
#         module = importlib.import_module(ipath)
#         func = getattr(module, func_name)
#     except Exception as exc:
#         raise ImportError(f'Could not import function from path: {import_path}')
#
#     return func
