import numpy as np
from roocs_utils.xarray_utils import xarray_utils as xu

from .common_utils import handle_derive_str


def squeeze_dims(ds_id, ds, **operands):
    """
    :param ds: Xarray Dataset
    :param operands: (dict) Arguments for fix. Dims (list) to remove.
    :return: Xarray Dataset
    """
    dims = operands.get("dims")
    for dim in dims:
        ds = ds.squeeze(dim)

    return ds


def add_scalar_coord(ds_id, ds, **operands):
    """
    :param ds: Xarray DataSet
    :param operands: sequence of arguments
    :return: Xarray Dataset
    Add a scalar coordinate.
    """
    var_id = operands.get("var_id")
    value = operands.get("value")
    dtype = operands.get("dtype")

    value = handle_derive_str(value, ds_id, ds)
    ds = ds.assign_coords({f"{var_id}": np.array(value, dtype=dtype)})

    for k, v in operands.get("attrs").items():
        v = handle_derive_str(v, ds_id, ds)
        ds[var_id].attrs[k] = v

    if operands.get("encoding"):
        for k, v in operands.get("encoding").items():
            v = handle_derive_str(v, ds_id, ds)
            ds[var_id].encoding[k] = v

    # update coordinates of main variable of dataset
    main_var = xu.get_main_variable(ds)
    main_var_coords = ds[main_var].encoding.get("coordinates", "")
    main_var_coords += f" {var_id}"
    ds[main_var].encoding["coordinates"] = main_var_coords

    return ds


def add_coord(ds_id, ds, **operands):
    """
    :param ds: Xarray DataSet
    :param operands: sequence of arguments
    :return: Xarray DataArray
    Add a coordinate.
    """
    var_id = operands.get("var_id")
    dim = operands.get("dim")
    value = operands.get("value")
    dtype = operands.get("dtype")

    value = handle_derive_str(value, ds_id, ds)
    ds = ds.assign_coords({f"{var_id}": (dim, np.array(value, dtype=dtype))})

    for k, v in operands.get("attrs").items():
        v = handle_derive_str(v, ds_id, ds)
        ds[var_id].attrs[k] = v

    for k, v in operands.get("encoding").items():
        v = handle_derive_str(v, ds_id, ds)
        ds[var_id].encoding[k] = v

    # update coordinates of main variable of dataset
    main_var = xu.get_main_variable(ds)
    main_var_coords = ds[main_var].encoding.get("coordinates", "")
    main_var_coords += f" {var_id}"
    ds[main_var].encoding["coordinates"] = main_var_coords

    return ds
