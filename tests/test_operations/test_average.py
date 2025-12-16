import os

from packaging.version import Version
import geopandas as gpd
import pytest
import xarray as xr
from daops import config_
from daops.ops.average import average_over_dims, average_shape, average_time
from clisops.exceptions import InvalidParameterValue
from shapely import Polygon
from xarray.coders import CFDatetimeCoder

TIME_CODER = CFDatetimeCoder(use_cftime=True)

CMIP5_IDS = [
    "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas",
    "cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh",
]
CMIP6_IDS = ["CMIP6.CMIP.CAS.FGOALS-g3.historical.r1i1p1f1.Amon.tas.gn.v20190818"]

POLY = Polygon(
    [
        [5.8671874999999996, 57.326521225217064],
        [-15.468749999999998, 48.45835188280866],
        [-16.171875, 24.84656534821976],
        [-3.8671874999999996, 13.581920900545844],
        [21.796875, 25.799891182088334],
        [22.8515625, 52.482780222078226],
        [5.8671874999999996, 57.326521225217064],
    ]
)


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
    ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)
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
    ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)
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
    ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)
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
def test_average_shape(tmpdir):
    xesmf = pytest.importorskip("xesmf")
    if Version(xesmf.__version__) < Version("0.8.2"):
        pytest.skip("Package xESMF >= 0.8.2 is required")

    # Save POLY to tmpdir
    tmp_poly_path = os.path.join(tmpdir, "tmppoly.json")
    gpd.GeoDataFrame([{"geometry": POLY}]).to_file(tmp_poly_path)

    result = average_shape(
        CMIP6_IDS[0],
        shape=tmp_poly_path,
        variable=None,
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)
    assert "geom" in ds.dims


@pytest.mark.online
def test_average_shape_none(tmpdir):
    with pytest.raises(InvalidParameterValue) as exc:
        result = average_shape(
            CMIP6_IDS[0],
            shape=None,
            variable=None,
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )
    assert str(exc.value) == "At least one area for averaging must be provided"


@pytest.mark.online
def test_average_time_month(tmpdir, mini_esgf_data):
    ds = xr.open_mfdataset(
        mini_esgf_data["CMIP5_DAY"], decode_times=TIME_CODER, combine="by_coords"
    )

    assert ds.time.shape == (3600,)
    assert ds.time.values[0].isoformat() == "2005-12-01T12:00:00"
    assert ds.time.values[-1].isoformat() == "2015-11-30T12:00:00"

    result = average_time(
        mini_esgf_data["CMIP5_DAY"],
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
    ds_res = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)

    assert ds_res.time.shape == (time_length,)
    assert ds_res.time.values[0].isoformat() == "2005-12-01T00:00:00"
    assert ds_res.time.values[-1].isoformat() == "2015-11-01T00:00:00"


@pytest.mark.online
def test_average_time_year(tmpdir, mini_esgf_data):
    # allow use of dataset - defaults to c3s-cmip6 and this is not in the catalog
    config_()["project:c3s-cmip6"]["use_catalog"] = False
    ds = xr.open_mfdataset(
        mini_esgf_data["CMIP6_MONTH"], decode_times=TIME_CODER, combine="by_coords"
    )

    assert ds.time.shape == (1980,)
    assert ds.time.values[0].isoformat() == "1850-01-16T12:00:00"
    assert ds.time.values[-1].isoformat() == "2014-12-16T12:00:00"

    result = average_time(
        mini_esgf_data["CMIP6_MONTH"],
        freq="year",
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)

    time_length = ds.time.values[-1].year - ds.time.values[0].year + 1

    # check only one output file
    assert len(result.file_uris) == 1
    ds_res = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)

    assert ds_res.time.shape == (time_length,)
    assert ds_res.time.values[0].isoformat() == "1850-01-01T00:00:00"
    assert ds_res.time.values[-1].isoformat() == "2014-01-01T00:00:00"
    config_()["project:c3s-cmip6"]["use_catalog"] = True


@pytest.mark.online
def test_average_time_incorrect_freq(tmpdir, mini_esgf_data):
    with pytest.raises(InvalidParameterValue) as exc:
        average_time(
            mini_esgf_data["CMIP5_DAY"],
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
def test_average_time_no_freq(tmpdir, mini_esgf_data):
    with pytest.raises(InvalidParameterValue) as exc:
        average_time(
            mini_esgf_data["CMIP5_DAY"],
            freq=None,
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )

    assert str(exc.value) == "At least one frequency for averaging must be provided"
