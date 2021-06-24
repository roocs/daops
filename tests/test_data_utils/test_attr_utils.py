import numpy as np
import xarray as xr

from daops.data_utils.attr_utils import remove_var_attrs
from tests._common import MINI_ESGF_MASTER_DIR


def test_remove_var_attrs(load_esgf_test_data):
    ds = xr.open_dataset(
        f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_EC-EARTH_historical_r1i1p1_185001-185912.nc",
        use_cftime=True,
    )

    assert ds.lat.attrs["standard_name"] == "latitude"
    assert ds.lat.attrs["long_name"] == "latitude"

    operands = {
        "var_id": "lat",
        "attrs": ["long_name", "standard_name"],
    }
    ds_remove_var_attrs = remove_var_attrs(ds, **operands)
    assert ds_remove_var_attrs.lat.attrs.get("standard_name", None) is None
    assert ds_remove_var_attrs.lat.attrs.get("long_name", None) is None
