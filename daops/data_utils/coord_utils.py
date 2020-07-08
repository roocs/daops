import numpy as np


def squeeze_dims(da, *args, **kwargs):
    """
    :param da: Xarray DataArray
    :param args: sequence of arguments
    :param kwargs: dictionary of arguments
    :return: Xarray DataArray
    """
    da_squeezed = da.squeeze(*args, **kwargs)
    return da_squeezed


def add_scalar_coord(ds, *args, **kwargs):
    """
    :param da: Xarray DataArray
    :param args: sequence of arguments
    :param kwargs: dictionary of arguments
    :return: Xarray DataArray
    """
    coord = kwargs.get('id')
    value = kwargs.get('value')
    dtype = kwargs.get('dtype')

    ds = ds.assign_coords({f'{coord}': np.array(value, dtype=dtype)})

    for k, v in kwargs.get('attrs').items():
        ds[coord].attrs[k] = v

    return ds