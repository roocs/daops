import numpy as np


def squeeze_dims(ds, **operands):
    """
    :param ds: Xarray DataSet
    :param operands: dictionary of arguments
    :return: Xarray DataArray
    """
    dims = operands.get("dims")
    for dim in dims:
        ds = ds.squeeze(dim)

    return ds


def add_scalar_coord(ds, **operands):
    """
    :param da: Xarray DataArray
    :param operands: dictionary of arguments
    :return: Xarray DataArray
    """
    coord = operands.get("id")
    value = operands.get("value")
    dtype = operands.get("dtype")

    ds = ds.assign_coords({f"{coord}": np.array(value, dtype=dtype)})

    for k, v in operands.get("attrs").items():
        ds[coord].attrs[k] = v

    return ds


def reverse_coords(ds, **operands):
    coords = operands.get("coords")

    for coord in coords:
        attrs = ds[coord].attrs
        ds = ds.assign_coords({f"{coord}": ds[coord].values[::-1]})
        ds[coord].attrs = attrs

    return ds
