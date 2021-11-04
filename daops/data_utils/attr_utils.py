from roocs_utils.xarray_utils import xarray_utils as xu

from .fix_utils import handle_derive_str


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


def remove_fill_values(ds_id, ds):
    """
    :param ds: Xarray Dataset
    :param operands: sequence of arguments
    :return: Xarray Dataset
    Remove _FillValue attribute that is added by xarray.
    """

    main_var = xu.get_main_variable(ds)
    for coord_id in ds[main_var].dims:
        if ds.coords[coord_id].dims == (coord_id,):
            ds[coord_id].encoding["_FillValue"] = None

    return ds


def remove_coord_attr(ds, **operands):
    """
    :param ds: Xarray DataSet
    :param operands: sequence of arguments
    :return: Xarray Dataset

    Remove coordinate attribute that is added by xarray, for specified variables.
    """

    var_ids = operands.get("var_ids")
    for v in var_ids:
        ds[v].encoding["coordinates"] = None

    return ds
