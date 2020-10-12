from roocs_utils.xarray_utils import xarray_utils as xu


def reverse_2d_vars(ds, **operands):
    var_ids = operands.get("var_ids")

    for var_id in var_ids:

        attrs = ds[var_id].attrs
        dims = ds[var_id].dims

        ds = ds.assign({f"{var_id}": (dims, ds[var_id].values[::-1, ::-1])})
        ds[var_id].attrs = attrs

    return ds
