import pytest
import xarray as xr
from daops.utils.core import Characterised, open_dataset
from xarray.coders import CFDatetimeCoder

TIME_CODER = CFDatetimeCoder(use_cftime=True)


class TestOpenDataset:

    ds_id = "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"

    def test_open_dataset_with_fix(self, stratus):
        fpath = (
            f"{stratus.path}/badc/cmip5/data/cmip5/output1/INM/inmcm4"
            "/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc"
        )

        unfixed_ds = xr.open_mfdataset(
            fpath, combine="by_coords", decode_times=TIME_CODER
        )
        fixed_ds = open_dataset(self.ds_id, fpath)
        assert unfixed_ds.sizes != fixed_ds.sizes
        assert "lev" in unfixed_ds.dims
        assert "lev" not in fixed_ds.dims

    def test_open_dataset_without_fix(self, stratus):
        fpath = (
            f"{stratus.path}/badc/cmip5/data/cmip5/output1/INM/inmcm4"
            "/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc"
        )

        ds = xr.open_mfdataset(fpath, combine="by_coords", decode_times=TIME_CODER)
        not_fixed_ds = open_dataset(self.ds_id, fpath, apply_fixes=False)
        assert ds.sizes == not_fixed_ds.sizes
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
