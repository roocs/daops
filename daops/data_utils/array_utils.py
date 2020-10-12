from roocs_utils.xarray_utils import xarray_utils as xu


def mask_data(ds, **operands):
    value = operands.get("value")
    var_id = xu.get_main_variable(ds)

    ds = ds.where(ds[var_id] != value)
    
    # dims = ds[var_id].dims
    # ds.assign({f"{var_id}": (dims, ds[var_id].to_masked_array())})

    return ds