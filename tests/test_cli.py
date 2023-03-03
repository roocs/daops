import xarray as xr
import pytest

from daops.ops.subset import subset

from roocs_utils.parameter import area_parameter
from roocs_utils.parameter import collection_parameter
from roocs_utils.parameter import time_parameter
from roocs_utils.parameter.param_utils import level_interval
from roocs_utils.parameter.param_utils import level_series
from roocs_utils.parameter.param_utils import time_components
from roocs_utils.parameter.param_utils import time_interval
from roocs_utils.parameter.param_utils import time_series

from tests.test_operations.test_subset import _check_output_nc


CMIP6_ID = "CMIP6.CMIP.NOAA-GFDL.GFDL-ESM4.historical.r1i1p1f1.Amon.o3.gr1.v20190726"


input_keys = ["collection", "time", "time_components", "area", "level"]
inputs = [
    ([CMIP6_ID, time_interval("1900-01-16", "1900-12-16"), None, (0, -10, 120, 40), level_interval(100000, 85000)],
        (12, 3, 1, 1)),
    ([CMIP6_ID, "1900-01-16/1900-12-16", None, (0, -10, 120, 40), level_interval(100000, 85000)],
        (12, 3, 1, 1)),
    ([CMIP6_ID, "1900-01-16/1900-12-16", None, "0,-10,120,40", "100000/85000"],
        (12, 3, 1, 1)),
    ([CMIP6_ID, "1900-01-16/1900-12-16", None, "0,-10,120,40", "100000,85000"],
        (12, 2, 1, 1)),
    ([CMIP6_ID, "1900-01-16/1901-12-16", "month:jan,apr,aug|year:1901", "0,-10,120,40", "100000,85000"],
        (3, 2, 1, 1)),
]


def _get_input_dict(args, **kwargs):
    d = {key: value for key, value in zip(input_keys, args)}
    d.update(**kwargs)
    return d


@pytest.mark.parametrize("args,expected_shape", inputs)
def test1(args, expected_shape, tmpdir, load_esgf_test_data):
    d = _get_input_dict(args, output_dir=tmpdir, file_namer="simple", apply_fixes=False)
    result = subset(**d)
    
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)
    assert ds.o3.shape == expected_shape
