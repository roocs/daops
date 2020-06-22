import collections
import xarray as xr

from daops.utils import fixer


def _wrap_sequence(obj):
    if isinstance(obj, str):
        obj = [obj]
    return obj


def is_dataref_characterised(data_ref):
    return True


def is_characterised(data_refs, require_all=False):
    """
    Takes in an individual data reference or a sequence of them.
    Returns an ordered dictionary of data_refs with a boolean value
    for each stating whether the dataset has been characterised.

    If `require_all` is True: return a single Boolean value.

    :param data_refs: one or more data references
    :param require_all: Boolean to require that all must be characterised
    :return: Ordered Dictionary OR Boolean (if `require_all` is True)
    """
    data_refs = _wrap_sequence(data_refs)
    resp = collections.OrderedDict()

    for dref in data_refs:
        _is_char = is_dataref_characterised(dref)

        if require_all and not _is_char:
            return False

        resp[dref] = is_dataref_characterised(dref)

    return resp


def open_dataset(ds_id, file_paths):
    # Wrap xarray open with required args

    fix = fixer.Fixer(ds_id)
    if fix.pre_processor:
        for pre_process in fix.pre_processors:
            print(f'[INFO] Loading data with pre_processor: {pre_process.__name__}')
    else:
        print(f'[INFO] Loading data')

    ds = xr.open_mfdataset(file_paths, preprocess=fix.pre_processor,
                           use_cftime=True, combine='by_coords')

    if fix.post_processor:
        for post_process in fix.post_processor:
            func, args, kwargs = post_process
            print(f'[INFO] Running post-processing function: {func.__name__}')
            ds = func(ds, *args, **kwargs)

    return ds
