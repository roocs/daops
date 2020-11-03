import xarray as xr

from daops.utils.core import open_dataset

fpath = (
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/INM/inmcm4"
    "/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc"
)
ds_id = "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"


def test_open_dataset_with_fix():
    unfixed_ds = xr.open_mfdataset(fpath, use_cftime=True, combine="by_coords")
    fixed_ds = open_dataset(ds_id, fpath)
    assert unfixed_ds.dims != fixed_ds.dims
    assert "lev" in unfixed_ds.dims
    assert "lev" not in fixed_ds.dims
