from daops.data_utils.var_utils import fix_metadata
from daops.ops.subset import subset

import xarray as xr


def test_add_scalar_coord():
    ds = xr.open_mfdataset(
        "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/ICHEC"
        "/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        combine="by_coords",
        use_cftime=True,
    )

    assert ds.tas.attrs["standard_name"] == "air_temperature"
    assert ds.tas.attrs["long_name"] == "Near-Surface Air Temperature"

    operands = {
        "fixes": [
                    "long_name,False long name",
                    "standard_name,fake_standard_name"
                ],
    }
    ds_change_metadata = fix_metadata(ds, **operands)
    assert ds_change_metadata.tas.attrs["standard_name"] == "fake_standard_name"
    assert ds_change_metadata.tas.attrs["long_name"] == "False long name"
