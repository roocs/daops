from roocs_utils.xarray_utils import xarray_utils as xu


def fix_attr_main_var(ds, **operands):
    """
    :param ds: Xarray DataSet
    :param operands: sequence of arguments
    :return: Xarray DataArray
    """
    var_id = xu.get_main_variable(ds)

    attrs = operands.get("attrs")
    for k, v in operands.get("attrs").items():
        ds[var_id].attrs[k] = v

    return ds


def fix_attr(ds, **operands):
    """
    :param ds: Xarray DataSet
    :param operands: sequence of arguments
    :return: Xarray DataArray
    """
    var_id = operands.get("var_id")

    attrs = operands.get("attrs")
    for k, v in operands.get("attrs").items():
        ds[var_id].attrs[k] = v

    return ds
