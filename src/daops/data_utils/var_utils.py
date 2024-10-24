import numpy as np


def add_data_var(ds_id, ds, **operands):
    """
    :param ds: Xarray DataSet
    :param operands: sequence of arguments
    :return: Xarray Dataset
    Add a data variable.
    """
    var_id = operands.get("var_id")
    value = operands.get("value")
    dtype = operands.get("dtype")

    ds = ds.assign({f"{var_id}": np.array(value, dtype=dtype)})

    for k, v in operands.get("attrs").items():
        ds[var_id].attrs[k] = v

    return ds
