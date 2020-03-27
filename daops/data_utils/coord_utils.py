

def squeeze_dims(da, *args, **kwargs):
    """

    :param ds: Xarray DataArray
    :param args: sequence of arguments
    :param kwargs: dictionary of arguments
    :return: Xarray DataArray
    """
    da_squeezed = da.squeeze(*args, **kwargs)
    return da_squeezed
