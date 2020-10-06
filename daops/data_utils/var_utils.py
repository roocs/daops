from roocs_utils.xarray_utils import xarray_utils as xu


def fix_metadata(ds, **operands):
    """
    :param ds: Xarray DataSet
    :param operands: sequence of arguments
    :return: Xarray DataArray
    """
    var_id = xu.get_main_variable(ds)

    fixes = operands.get("fixes")
    for fix in fixes:
        attr, value = fix.split(',')
        ds[var_id].attrs[attr] = value

    return ds
