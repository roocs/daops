import os

import pytest
import xarray as xr

# from daops.ops.regrid import regrid

# TODO: remove when upgraded to new clisops version
# pytestmark = pytest.mark.xfail(reason="needs clisops>=0.12 with regrid operator")

CMIP6_IDS = ["CMIP6.CMIP.MPI-M.MPI-ESM1-2-HR.historical.r1i1p1f1.Omon.tos.gn.v20190710"]


def _check_output_nc(result, fname="output_001.nc"):
    assert fname in [os.path.basename(_) for _ in result.file_uris]


@pytest.mark.online
def test_regrid(tmpdir, load_esgf_test_data):
    from daops.ops.regrid import regrid

    result = regrid(
        CMIP6_IDS[0],
        method="conservative",
        adaptive_masking_threshold=0.5,
        grid="1deg",
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )

    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)
    assert "time" in ds.dims
    assert "tos" in ds
