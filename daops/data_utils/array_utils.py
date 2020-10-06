from roocs_utils.xarray_utils import xarray_utils as xu


def mask_missing_data(ds, **operands):
    var_id = xu.get_main_variable(ds)
    ds[var_id].data = ds[var_id].data + args[0]
    return ds