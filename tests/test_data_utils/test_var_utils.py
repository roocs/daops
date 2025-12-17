import xarray as xr
from daops.data_utils.var_utils import add_data_var


def test_add_data_var(stratus):
    time_coder = xr.coders.CFDatetimeCoder(use_cftime=True)
    ds = xr.open_mfdataset(
        f"{stratus.path}/badc/cmip5/data/cmip5/output1/INM/"
        "inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc",
        combine="by_coords",
        decode_times=time_coder,
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
