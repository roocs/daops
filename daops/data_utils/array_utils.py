from roocs_utils.xarray_utils import xarray_utils as xu


def mask_data(ds, **operands):
    value = operands.get("value")
    var_id = xu.get_main_variable(ds)

    ds = ds.where(ds[var_id] != value)

    return ds
