def remove_var_attrs(ds, **operands):
    """
    :param ds: Xarray DataSet
    :param operands: sequence of arguments
    :return: Xarray Dataset

    Change the attributes of a variable.
    """
    var_id = operands.get("var_id")

    attrs = operands.get("attrs")
    for attr in operands.get("attrs"):
        ds[var_id].attrs.pop(attr)

    return ds
