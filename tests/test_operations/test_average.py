import os

import pytest
import xarray as xr
from roocs_utils.exceptions import InvalidParameterValue

from daops import CONFIG
from daops.ops.average import average_over_dims
from daops.ops.average import average_time
from tests._common import CMIP5_DAY
from tests._common import CMIP6_MONTH

CMIP5_IDS = [
    "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas",
    "cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh",
]


def _check_output_nc(result, fname="output_001.nc"):
    assert fname in [os.path.basename(_) for _ in result.file_uris]


@pytest.mark.online
def test_average_dims_time(tmpdir):
    result = average_over_dims(
        CMIP5_IDS[1],
        dims=["time"],
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)
    assert "time" not in ds.dims


@pytest.mark.online
def test_average_time_lat(tmpdir):
    result = average_over_dims(
        CMIP5_IDS[1],
        dims=["latitude", "time"],
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)
    assert "time" not in ds.dims
    assert "lat" not in ds.dims


@pytest.mark.online
def test_average_time_lon(tmpdir):
    result = average_over_dims(
        CMIP5_IDS[1],
        dims=["time", "longitude"],
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)
    assert "time" not in ds.dims
    assert "lon" not in ds.dims


@pytest.mark.online
def test_average_none(tmpdir):
    with pytest.raises(InvalidParameterValue) as exc:
        average_over_dims(
            CMIP5_IDS[1],
            dims=None,
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )
    assert str(exc.value) == "At least one dimension for averaging must be provided"


@pytest.mark.online
def test_average_level(tmpdir):
    with pytest.raises(InvalidParameterValue) as exc:
        average_over_dims(
            CMIP5_IDS[1],
            dims=["level"],
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )
    assert (
        str(exc.value)
        == "Requested dimensions were not found in input dataset: {'level'}."
    )


@pytest.mark.online
def test_average_time_month(tmpdir):
    ds = xr.open_mfdataset(CMIP5_DAY, use_cftime=True, combine="by_coords")

    assert ds.time.shape == (3600,)
    assert ds.time.values[0].isoformat() == "2005-12-01T12:00:00"
    assert ds.time.values[-1].isoformat() == "2015-11-30T12:00:00"

    result = average_time(
        CMIP5_DAY,
        freq="month",
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)

    time_length = (
        ds.time.values[-1].year - ds.time.values[0].year
    ) * 12  # get number of months

    # check only one output file
    assert len(result.file_uris) == 1
    ds_res = xr.open_dataset(result.file_uris[0], use_cftime=True)

    assert ds_res.time.shape == (time_length,)
    assert ds_res.time.values[0].isoformat() == "2005-12-01T00:00:00"
    assert ds_res.time.values[-1].isoformat() == "2015-11-01T00:00:00"


@pytest.mark.online
def test_average_time_year(tmpdir):
    # allow use of dataset - defaults to c3s-cmip6 and this is not in the catalog
    CONFIG["project:c3s-cmip6"]["use_catalog"] = False
    ds = xr.open_mfdataset(CMIP6_MONTH, use_cftime=True, combine="by_coords")

    assert ds.time.shape == (1980,)
    assert ds.time.values[0].isoformat() == "1850-01-16T12:00:00"
    assert ds.time.values[-1].isoformat() == "2014-12-16T12:00:00"

    result = average_time(
        CMIP6_MONTH,
        freq="year",
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)

    time_length = ds.time.values[-1].year - ds.time.values[0].year + 1

    # check only one output file
    assert len(result.file_uris) == 1
    ds_res = xr.open_dataset(result.file_uris[0], use_cftime=True)

    assert ds_res.time.shape == (time_length,)
    assert ds_res.time.values[0].isoformat() == "1850-01-01T00:00:00"
    assert ds_res.time.values[-1].isoformat() == "2014-01-01T00:00:00"
    CONFIG["project:c3s-cmip6"]["use_catalog"] = True


@pytest.mark.online
def test_average_time_incorrect_freq(tmpdir):
    with pytest.raises(InvalidParameterValue) as exc:
        average_time(
            CMIP5_DAY,
            freq="week",
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )

    assert (
        str(exc.value)
        == "Time frequency for averaging must be one of ['day', 'month', 'year']."
    )


@pytest.mark.online
def test_average_time_no_freq(tmpdir):
    with pytest.raises(InvalidParameterValue) as exc:
        average_time(
            CMIP5_DAY,
            freq=None,
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )

    assert str(exc.value) == "At least one frequency for averaging must be provided"
