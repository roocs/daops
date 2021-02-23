import pytest
import xarray as xr

from daops.utils.core import Characterised
from daops.utils.core import open_dataset

from tests._common import MINI_ESGF_MASTER_DIR

fpath = (
    f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/INM/inmcm4"
    "/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc"
)
ds_id = "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"


def test_open_dataset_with_fix(load_esgf_test_data):
    unfixed_ds = xr.open_mfdataset(fpath, use_cftime=True, combine="by_coords")
    fixed_ds = open_dataset(ds_id, fpath)
    assert unfixed_ds.dims != fixed_ds.dims
    assert "lev" in unfixed_ds.dims
    assert "lev" not in fixed_ds.dims


def test_open_dataset_without_fix(load_esgf_test_data):
    ds = xr.open_mfdataset(fpath, use_cftime=True, combine="by_coords")
    not_fixed_ds = open_dataset(ds_id, fpath, apply_fixes=False)
    assert ds.dims == not_fixed_ds.dims
    assert "lev" in ds.dims
    assert "lev" in not_fixed_ds.dims


@pytest.mark.online
def test_is_characterised():
    dset = "cmip5.output1.CCCma.CanCM4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    result = Characterised(dset).lookup_characterisation()
    assert result is True

    dset = "c3s-cmip5.output1.ICHEC.EC-EARTH.historical.day.atmos.day.r1i1p1.tas.latest"
    result = Characterised(dset).lookup_characterisation()
    assert result is False
