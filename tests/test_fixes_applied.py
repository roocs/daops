import math
import os

import cftime
import numpy as np
import pytest
import xarray as xr

from daops.ops.subset import subset
from tests._common import CMIP6_DECADAL
from tests._common import MINI_ESGF_MASTER_DIR


def _check_output_nc(result, fname="output_001.nc"):
    assert fname in [os.path.basename(_) for _ in result.file_uris]


@pytest.mark.online
def test_fixes_applied_decadal_data(tmpdir, load_esgf_test_data):

    result = subset(
        CMIP6_DECADAL,
        output_dir=tmpdir,
        file_namer="simple",
    )

    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True, decode_timedelta=False)

    # check VarAttrFix is applied
    assert ds.time.long_name == "valid_time"

    # check GlobalAttrFix is applied
    assert ds.forcing_description == "Free text describing the forcings"
    assert (
        ds.initialization_description
        == "Free text describing the initialization method"
    )
    assert ds.physics_description == "Free text describing the physics method"
    assert ds.startdate == "s200411"
    assert ds.sub_experiment_id == "s200411"

    # check AddScalarCoord Fix is applied
    assert "reftime" in ds.coords
    assert ds.reftime.dims == ()
    assert ds.reftime.values == np.array(
        cftime.DatetimeGregorian(2004, 11, 1, 0, 0, 0, 0), dtype=object
    )

    # check AddCoordFix is applied
    assert "leadtime" in ds.coords
    assert ds.leadtime.dims == ("time",)
    assert ds.leadtime.values[0] == 15.0
    assert ds.leadtime.values[-1] == 3787.0
    assert ds.leadtime.units == "days"
    assert ds.leadtime.long_name == "Time elapsed since the start of the forecast"
    assert ds.leadtime.standard_name == "forecast_period"

    # check AddDataVarFix is applied
    assert "realization" in ds.data_vars
    assert ds.realization.values == np.array(1, dtype=np.int32)
    assert (
        ds.realization.comment
        == "For more information on the ripf, refer to the variant_label, initialization_description, physics_description and forcing_description global attributes"
    )

    # check RemoveFillValuesFix is applied
    # assert no fill value for coordinate variables
    assert ds.lon.encoding.get("_FillValue") is None
    assert ds.lat.encoding.get("_FillValue") is None
    assert ds.time.encoding.get("_FillValue") is None

    # compare to e.g. lon_bnds where the fill value is added by xarray but we haven't removed it
    assert math.isnan(ds.lon_bnds.encoding.get("_FillValue"))
