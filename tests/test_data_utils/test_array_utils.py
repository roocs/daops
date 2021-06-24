import numpy as np
import pytest
import xarray as xr

from daops.data_utils.array_utils import replace_lat_and_lon_fill_values
from tests._common import MINI_ESGF_MASTER_DIR


def test_replace_lat_and_lon_fill_values(load_esgf_test_data, tmpdir):
    ds = xr.open_dataset(
        f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip6/data/CMIP6/CMIP/SNU/SAM0-UNICON/historical/r1i1p1f1/SImon/siconc/gn/latest/siconc_SImon_SAM0-UNICON_historical_r1i1p1f1_gn_185001-185912.nc",
        use_cftime=True,
    )

    # lat and lon have large max values - fill value has not been masked properly
    assert float(ds.longitude.max()) == 1.0000000150474662e30
    assert float(ds.latitude.max()) == 1.0000000150474662e30

    operands = {"value": "1.0000000150474662e+30"}

    ds = replace_lat_and_lon_fill_values(ds, **operands)

    # check the values have been masked and fill value set
    assert ds.latitude.values.max() == 1e20
    assert ds.longitude.values.max() == 1e20

    ds.latitude.encoding.get("_FillValue") == 1e20
    ds.longitude.encoding.get("_FillValue") == 1e20

    # save to netcdf and reload to check max/min is now correct
    ds.to_netcdf(f"{tmpdir}/replace_fill_value.nc")

    ds = xr.open_dataset(f"{tmpdir}/replace_fill_value.nc", use_cftime=True)

    assert float(ds.longitude.max()) == 320.5625
    assert float(ds.latitude.max()) == 46.32559585571289
