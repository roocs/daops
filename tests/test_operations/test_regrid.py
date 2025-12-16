import os

from packaging.version import Version
import pytest
import xarray as xr


CMIP6_IDS = ["CMIP6.CMIP.MPI-M.MPI-ESM1-2-HR.historical.r1i1p1f1.Omon.tos.gn.v20190710"]


def _check_output_nc(result, fname="output_001.nc"):
    assert fname in [os.path.basename(_) for _ in result.file_uris]


@pytest.mark.slow
def test_regrid(tmpdir):
    xesmf = pytest.importorskip("xesmf")
    if Version(xesmf.__version__) < Version("0.8.2"):
        pytest.skip("Package xESMF >= 0.8.2 is required")

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
    time_coder = xr.coders.CFDatetimeCoder(use_cftime=True)
    ds = xr.open_dataset(result.file_uris[0], decode_times=time_coder)
    assert "time" in ds.dims
    assert "tos" in ds
