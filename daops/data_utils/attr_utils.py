from roocs_utils.xarray_utils import xarray_utils as xu

from .common_utils import handle_derive_str


def edit_var_attrs(ds_id, ds, **operands):
    """
    :param ds: Xarray DataSet
    :param operands: sequence of arguments
    :return: Xarray Dataset
    Change the attributes of a variable.
    """
    var_id = operands.get("var_id")

    attrs = operands.get("attrs")
    for k, v in operands.get("attrs").items():
        v = handle_derive_str(v, ds_id, ds)
        ds[var_id].attrs[k] = v

    return ds


def edit_global_attrs(ds_id, ds, **operands):
    """
    :param ds: Xarray DataSet
    :param operands: sequence of arguments
    :return: Xarray DataArray
    Change the gloabl attributes.
    """
    attrs = operands.get("attrs")

    for k, v in operands.get("attrs").items():
        v = handle_derive_str(v, ds_id, ds)
        ds.attrs[k] = v

    return ds


def add_global_attrs_if_needed(ds_id, ds, **operands):
    """
    :param ds: Xarray DataSet
    :param operands: sequence of arguments
    :return: Xarray Dataset
    Add a global attribute if it doesn't already exist.
    """

    attrs = operands.get("attrs")
    for k, v in operands.get("attrs").items():
        # check if the key already exists before setting it
        v = handle_derive_str(v, ds_id, ds)
        if not ds.attrs.get(k, None):
            ds.attrs[k] = v

    return ds


def remove_coord_attr(ds_id, ds, **operands):
    """
    :param ds: Xarray DataSet
    :param operands: sequence of arguments
    :return: Xarray Dataset

    Remove coordinate attribute that is added by xarray, for specified variables.
    """
    var_ids = handle_derive_str(operands.get("var_ids"), ds_id, ds)

    for v in var_ids:
        ds[v].encoding["coordinates"] = None

    return ds
