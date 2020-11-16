import numpy as np


def squeeze_dims(ds, **operands):
    """
    :param ds: Xarray Dataset
    :param operands: (dict) Arguments for fix. Dims (list) to remove.
    :return: Xarray Dataset
    """
    dims = operands.get("dims")
    for dim in dims:
        ds = ds.squeeze(dim)

    return ds


def add_scalar_coord(ds, **operands):
    """
    :param ds: Xarray Dataset
    :param operands: (dict) Arguments for fix. Id, value and data type of scalar coordinate to add.
    :return: Xarray Dataset
    """
    coord = operands.get("id")
    value = operands.get("value")
    dtype = operands.get("dtype")

    ds = ds.assign_coords({f"{coord}": np.array(value, dtype=dtype)})

    for k, v in operands.get("attrs").items():
        ds[coord].attrs[k] = v

    return ds
