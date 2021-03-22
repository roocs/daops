import os

import pytest
import xarray as xr
from roocs_utils.exceptions import InvalidParameterValue

from daops import CONFIG
from daops.ops.regrid import regrid

CMIP5_IDS = [
    "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas",
    "cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh",
]


def _check_output_nc(result, fname="output_001.nc"):
    assert fname in [os.path.basename(_) for _ in result.file_uris]


@pytest.mark.online
def test_regrid(tmpdir):
    result = regrid(
        CMIP5_IDS[1],
        method="nn",
        adaptive_masking_threshold=0.5,
        grid="1deg",
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)
