"""Module for editing the attributes of a dataset."""

from .common_utils import handle_derive_str


def edit_var_attrs(ds_id, ds, **operands):
    """
    Edit the variable attrs.

    Parameters
    ----------
    ds_id : str
        Dataset ID.
    ds : xarray.Dataset
        A Dataset.
    operands : dict
        Dictionary containing the new attributes for the variable.

    Returns
    -------
    xarray.Dataset
    """
    var_id = operands.get("var_id")

    operands.get("attrs")
    for k, v in operands.get("attrs").items():
        v = handle_derive_str(v, ds_id, ds)
        ds[var_id].attrs[k] = v

    return ds


def edit_global_attrs(ds_id, ds, **operands):
    """
    Edit the global attrs.

    Parameters
    ----------
    ds_id : str
        Dataset ID.
    ds : xarray.Dataset
        A Dataset.
    operands : dict
        Dictionary containing the new attributes for the dataset.

    Returns
    -------
    xarray.Dataset
    """
    operands.get("attrs")

    for k, v in operands.get("attrs").items():
        v = handle_derive_str(v, ds_id, ds)
        ds.attrs[k] = v

    return ds


def add_global_attrs_if_needed(ds_id, ds, **operands):
    """
    Add the global attrs, if needed.

    Parameters
    ----------
    ds_id : str
        Dataset ID.
    ds : xarray.Dataset
        A Dataset.
    operands : dict
        Dictionary containing the new attributes for the dataset.

    Returns
    -------
    xarray.Dataset
    """
    operands.get("attrs")
    for k, v in operands.get("attrs").items():
        # check if the key already exists before setting it
        v = handle_derive_str(v, ds_id, ds)
        if not ds.attrs.get(k, None):
            ds.attrs[k] = v

    return ds


def remove_coord_attr(ds_id, ds, **operands):
    """
    Remove the coordinate attr from the dataset.

    Parameters
    ----------
    ds_id : str
        Dataset ID.
    ds : xarray.Dataset
        A Dataset.
    operands : dict
        Dictionary containing the new attributes for the dataset.

    Returns
    -------
    xarray.Dataset
    """
    var_ids = handle_derive_str(operands.get("var_ids"), ds_id, ds)

    for v in var_ids:
        ds[v].encoding["coordinates"] = None

    return ds
