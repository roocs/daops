import xarray as xr

from daops.data_utils.attr_utils import fix_attr
from daops.data_utils.attr_utils import fix_attr_main_var
from daops.ops.subset import subset
from tests._common import MINI_ESGF_MASTER_DIR


def test_fix_attr_main_var(load_esgf_test_data):
    ds = xr.open_mfdataset(
        f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/ICHEC"
        "/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        combine="by_coords",
        use_cftime=True,
    )

    assert ds.tas.attrs["standard_name"] == "air_temperature"
    assert ds.tas.attrs["long_name"] == "Near-Surface Air Temperature"

    operands = {
        "attrs": {
            "long_name": "False long name",
            "standard_name": "fake_standard_name",
        },
    }
    ds_change_metadata = fix_attr_main_var(ds, **operands)
    assert ds_change_metadata.tas.attrs["standard_name"] == "fake_standard_name"
    assert ds_change_metadata.tas.attrs["long_name"] == "False long name"


def test_fix_attr_var(load_esgf_test_data):
    ds = xr.open_mfdataset(
        f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/ICHEC"
        "/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        combine="by_coords",
        use_cftime=True,
    )

    assert ds.lat.attrs["standard_name"] == "latitude"
    assert ds.lat.attrs["long_name"] == "latitude"

    operands = {
        "var_id": "lat",
        "attrs": {
            "long_name": "False long name",
            "standard_name": "fake_standard_name",
        },
    }
    ds_change_metadata = fix_attr(ds, **operands)
    assert ds_change_metadata.lat.attrs["standard_name"] == "fake_standard_name"
    assert ds_change_metadata.lat.attrs["long_name"] == "False long name"
