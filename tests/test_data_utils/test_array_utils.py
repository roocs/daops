import numpy as np
import xarray as xr

from daops.data_utils.array_utils import mask_data
from tests._common import MINI_ESGF_MASTER_DIR


def test_mask_data(load_esgf_test_data):
    ds = xr.open_mfdataset(
        f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/ICHEC"
        "/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        combine="by_coords",
        use_cftime=True,
    )

    assert ds.tas.values[0][0][0] == np.float32(246.3239)
    assert np.isclose(ds.tas.values[0][0][0], 246.3239)

    operands = {
        "value": 246.3239,
    }
    ds_mask_data = mask_data(ds, **operands)
    np.testing.assert_equal(ds_mask_data.tas.values[0][0][0], np.nan)
