from daops.data_utils.coord_utils import squeeze_dims, add_scalar_coord, reverse_coords

import xarray as xr
import numpy as np


def test_squeeze_dims():
    ds = xr.open_mfdataset(
        "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/INM/"
        "inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc",
        combine="by_coords",
        use_cftime=True,
    )

    assert "lev" in ds.dims

    operands = {
        "dims": ["lev"]
    }

    ds_squeeze = squeeze_dims(ds, **operands)
    assert "lev" not in ds_squeeze.dims


def test_add_scalar_coord():
    ds_no_height = xr.open_mfdataset(
        "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/ICHEC/EC-EARTH/"
        "historical/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        combine="by_coords",
        use_cftime=True,
    )
    ds_with_height = xr.open_mfdataset(
        "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/INM/inmcm4"
        "/historical/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        combine="by_coords",
        use_cftime=True,
    )
    operands = {
        "dtype": "float64",
        "value": 2.0,
        "id": "height",
        "length": 1,
        "attrs": {
            "axis": "Z",
            "long_name": "height",
            "positive": "up",
            "standard_name": "height",
            "units": "m",
        },
    }
    ds_no_height = add_scalar_coord(ds_no_height, **operands)
    assert ds_no_height.height == ds_with_height.height
    assert ds_no_height.height.attrs == ds_with_height.height.attrs


def test_reverse_coords():
    ds = xr.open_mfdataset(
        "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/ICHEC"
        "/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        combine="by_coords",
        use_cftime=True,
    )

    assert np.isclose(ds.lon.values[0], 0)
    assert np.isclose(ds.lon.values[-1], 337.5)

    operands = {
        "coords": ['lon']
    }

    ds_reverse_lon = reverse_coords(ds, **operands)

    assert np.isclose(ds_reverse_lon.lon.values[0], 337.5)
    assert np.isclose(ds_reverse_lon.lon.values[-1], 0)
