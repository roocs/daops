import xarray as xr

from daops.data_utils.var_utils import add_data_var
from tests._common import MINI_ESGF_MASTER_DIR


def test_add_data_var(load_esgf_test_data):
    ds = xr.open_mfdataset(
        f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/INM/"
        "inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc",
        combine="by_coords",
        use_cftime=True,
    )

    ds_id = "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"

    assert "realization" not in ds.data_vars

    operands = {
        "var_id": "realization",
        "value": "1",
        "dtype": "int32",
        "attrs": {"long_name": "realization", "comment": "example"},
    }

    ds = add_data_var(ds_id, ds, **operands)
    assert "realization" in ds.data_vars
