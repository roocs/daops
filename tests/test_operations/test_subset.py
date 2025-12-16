import os

import numpy as np
import pytest
import xarray as xr
from daops import config_
from daops.ops.subset import subset
from clisops.exceptions import InvalidParameterValue, MissingParameterValue
from clisops.parameter import area_parameter, collection_parameter, time_parameter
from clisops.parameter import (
    level_interval,
    level_series,
    time_components,
    time_interval,
    time_series,
)
from clisops.utils.file_utils import FileMapper
from xarray.coders import CFDatetimeCoder

TIME_CODER = CFDatetimeCoder(use_cftime=True)

CMIP5_IDS = [
    "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas",
    "cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh",
]

CMIP6_IDS = ["CMIP6.CMIP.NOAA-GFDL.GFDL-ESM4.historical.r1i1p1f1.Amon.o3.gr1.v20190726"]

C3S_CMIP6_IDS = [
    "c3s-cmip6.CMIP.MPI-M.MPI-ESM1-2-HR.historical.r1i1p1f1.Amon.tasmin.gn.v20190710",
]

zostoga_ids = [
    "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.BCC.bcc-csm1-1.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MOHC.HadGEM2-ES.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.CCCma.CanCM4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.IPSL.IPSL-CM5A-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
]


def _check_output_nc(result, fname="output_001.nc"):
    assert fname in [os.path.basename(_) for _ in result.file_uris]


@pytest.mark.online
def test_subset_zostoga_with_fix(tmpdir):
    result = subset(
        CMIP5_IDS[0],
        time=time_interval("2085-01-16", "2120-12-16"),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=True,
    )

    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)
    assert ds.time.shape == (192,)
    assert "lev" not in ds.dims


def test_subset_zostoga_with_apply_fixes_false(tmpdir, load_test_data):
    result = subset(
        CMIP5_IDS[0],
        time=time_interval("2085-01-16", "2120-12-16"),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)
    assert ds.time.shape == (192,)

    # lev should still be in ds.dims because fix hasn't been applied
    assert "lev" in ds.dims


@pytest.mark.xfail(reason="skip due to issues with chunks")
def test_subset_t(tmpdir, load_test_data):
    result = subset(
        CMIP5_IDS[1],
        time=time_interval("2085-01-16", "2120-12-16"),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)
    assert ds.time.shape == (433,)


@pytest.mark.skip(reason="test service is not available")
@pytest.mark.online
def test_subset_t_kerchunk(tmpdir, cmip6_kerchunk_https_open_json):
    result = subset(
        cmip6_kerchunk_https_open_json,
        time=time_interval("1948-01-16", "1952-12-16"),
        area=(0, -10, 120, 40),
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)
    assert ds.time.shape == (60,)
    assert ds.tasmax.shape == (60, 40, 64)
    assert np.isclose(float(ds.tasmax.max()), 327.24411011)


# @pytest.mark.online
def test_subset_no_collection(tmpdir):
    with pytest.raises(TypeError):
        subset(
            time=time_interval("2085-01-16", "2120-12-16"),
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )


# @pytest.mark.online
def test_subset_collection_as_none(tmpdir):
    with pytest.raises(InvalidParameterValue):
        subset(
            None,
            time=time_interval("2085-01-16", "2120-12-16"),
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )


# @pytest.mark.online
def test_subset_collection_as_empty_string(tmpdir):
    with pytest.raises(MissingParameterValue):
        subset(
            "",
            time=time_interval("2085-01-16", "2120-12-16"),
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )


@pytest.mark.xfail(reason="skip due to issues with chunks")
def test_subset_t_y_x(tmpdir, stratus):
    fpath = f"{stratus.path}/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc"

    ds = xr.open_mfdataset(
        fpath,
        combine="by_coords",
        data_vars="all",
        decode_times=TIME_CODER,
    )
    assert ds.tas.shape == (3530, 2, 2)

    result = subset(
        CMIP5_IDS[1],
        time=time_interval("2085-01-16", "2120-12-16"),
        area=(0, -10, 120, 40),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)

    ds_subset = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)
    assert ds_subset.tas.shape == (433, 1, 1)


# @pytest.mark.online
def test_subset_t_z_y_x(tmpdir, stratus):
    fpath = (
        f"{stratus.path}/badc/cmip6/data/CMIP6/CMIP/NOAA-GFDL/"
        "GFDL-ESM4/historical/r1i1p1f1/Amon/o3/gr1/v20190726/"
        "o3_Amon_GFDL-ESM4_historical_r1i1p1f1_gr1_185001-194912.nc"
    )

    ds = xr.open_mfdataset(
        fpath,
        decode_times=TIME_CODER,
        combine="by_coords",
    )

    assert ds.o3.shape == (1200, 19, 2, 3)
    np.testing.assert_array_equal(
        ds.o3.coords["plev"],
        [
            100000.0,
            92500.0,
            85000.0,
            70000.0,
            60000.0,
            50000.0,
            40000.0,
            30000.0,
            25000.0,
            20000.0,
            15000.0,
            10000.0,
            7000.0,
            5000.0,
            3000.0,
            2000.0,
            1000.0,
            500.0,
            100.0,
        ],
    )

    result = subset(
        CMIP6_IDS[0],
        time=time_interval("1900-01-16", "1900-12-16"),
        area=(0, -10, 120, 40),
        level=level_interval(10000, 850.0),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)

    ds_subset = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)
    assert ds_subset.o3.shape == (12, 6, 1, 1)


# @pytest.mark.online
def test_subset_t_with_invalid_date(tmpdir, load_test_data):
    with pytest.raises(Exception) as exc:
        subset(
            CMIP5_IDS[1],
            time=time_interval("1985-01-16", "2002-12-16"),
            area=("0", "-10", "120", "40"),
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )
    assert (
        str(exc.value) == "No files found in given time range for "
        "cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas"
    )


@pytest.fixture(
    params=[
        zostoga_ids[0],
        zostoga_ids[1],
        zostoga_ids[2],
        zostoga_ids[3],
        zostoga_ids[4],
        zostoga_ids[5],
    ]
)
def zostoga_id(request):
    id = request.param
    return id


@pytest.mark.online
def test_subset_with_fix_and_multiple_ids(zostoga_id, tmpdir):
    result = subset(
        zostoga_id,
        time=time_interval("2008-01-16", "2028-12-16"),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=True,
    )
    _check_output_nc(result)

    ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)
    assert ds.time.shape in [(251,), (252,)]
    assert "lev" not in ds.dims  # checking that lev has been removed by fix
    ds.close()


@pytest.mark.xfail(reason="skip due to issues with chunks")
def test_parameter_classes_as_args(tmpdir, load_test_data):
    collection = collection_parameter.CollectionParameter(CMIP5_IDS[1])
    time = time_parameter.TimeParameter(time_interval("2085-01-16", "2120-12-16"))
    area = area_parameter.AreaParameter((0, -10, 120, 40))

    result = subset(
        collection, time=time, area=area, output_dir=tmpdir, file_namer="simple"
    )
    _check_output_nc(result)

    ds_subset = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)
    assert ds_subset.tas.shape == (433, 1, 1)


@pytest.mark.xfail(reason="skip due to issues with chunks")
def test_time_is_none(tmpdir, load_test_data):
    result = subset(
        CMIP5_IDS[1],
        time=None,
        area=("0", "-10", "120", "40"),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )

    _check_output_nc(result)

    ds = xr.open_mfdataset(
        os.path.join(
            config_()["project:cmip5"]["base_dir"],
            "output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        ),
        data_vars="all",
        decode_times=TIME_CODER,
    )
    ds_subset = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)

    assert ds_subset.time.values.min().strftime(
        "%Y-%m-%d"
    ) == ds.time.values.min().strftime("%Y-%m-%d")
    assert ds_subset.time.values.max().strftime(
        "%Y-%m-%d"
    ) == ds.time.values.max().strftime("%Y-%m-%d")


@pytest.mark.xfail(reason="skip due to issues with chunks")
def test_end_time_is_none(tmpdir, load_test_data):
    result = subset(
        CMIP5_IDS[2],
        time=time_interval("1940-10-14/"),
        area=("0", "-10", "120", "40"),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)

    ds = xr.open_mfdataset(
        os.path.join(
            config_()["project:cmip5"]["base_dir"],
            "output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/latest/rh/*.nc",
        ),
        data_vars="all",
        decode_times=TIME_CODER,
    )
    ds_subset = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)

    assert ds_subset.time.values.min().strftime("%Y-%m-%d") == "1940-10-16"
    assert ds_subset.time.values.max().strftime(
        "%Y-%m-%d"
    ) == ds.time.values.max().strftime("%Y-%m-%d")


@pytest.mark.xfail(reason="skip due to issues with chunks")
def test_start_time_is_none(tmpdir, load_test_data):
    result = subset(
        CMIP5_IDS[1],
        time=time_interval("/2120-12-16"),
        area=("0", "-10", "120", "40"),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)

    ds = xr.open_mfdataset(
        os.path.join(
            config_()["project:cmip5"]["base_dir"],
            "output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        ),
        data_vars="all",
        decode_times=TIME_CODER,
    )
    ds_subset = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)

    assert ds_subset.time.values.min().strftime(
        "%Y-%m-%d"
    ) == ds.time.values.min().strftime("%Y-%m-%d")
    assert ds_subset.time.values.max().strftime("%Y-%m-%d") == "2120-12-16"


# @pytest.mark.online
def test_time_invariant_subset_standard_name(tmpdir, load_test_data):
    dset = "CMIP6.ScenarioMIP.IPSL.IPSL-CM6A-LR.ssp119.r1i1p1f1.fx.mrsofc.gr.v20190410"

    result = subset(
        dset,
        area=(5.0, 10.0, 300.0, 80.0),
        output_dir=tmpdir,
        output_type="nc",
        file_namer="standard",
        apply_fixes=False,
    )

    assert "mrsofc_fx_IPSL-CM6A-LR_ssp119_r1i1p1f1_gr.nc" in result.file_uris[0]


# @pytest.mark.online
def test_subset_with_file_mapper(tmpdir, stratus):
    file_paths = [
        f"{stratus.path}/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES"
        f"/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_200512-203011.nc",
        f"{stratus.path}/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES"
        f"/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_203012-205511.nc",
    ]

    dset = FileMapper(file_paths)

    result = subset(
        dset,
        time=time_interval("2008-01-16", "2028-12-16"),
        output_dir=tmpdir,
        output_type="nc",
        file_namer="standard",
        apply_fixes=False,
    )

    assert "tas_mon_HadGEM2-ES_rcp85_r1i1p1_20080116-20281216.nc" in result.file_uris[0]


# @pytest.mark.online
def test_subset_with_catalog(tmpdir, load_test_data):
    # c3s-cmip6 dataset so will use catalog in consolidate
    result = subset(
        "c3s-cmip6.ScenarioMIP.INM.INM-CM5-0.ssp245.r1i1p1f1.Amon.rlds.gr1.v20190619",
        time=time_interval("2028-01-16", "2050-12-16"),
        output_dir=tmpdir,
        output_type="nc",
        file_namer="standard",
        apply_fixes=False,
    )

    _check_output_nc(
        result, fname="rlds_Amon_INM-CM5-0_ssp245_r1i1p1f1_gr1_20280116-20501216.nc"
    )


# @pytest.mark.online
def test_subset_with_catalog_time_invariant(tmpdir, load_test_data):
    # c3s-cmip6 dataset so will use catalog in consolidate
    result = subset(
        "c3s-cmip6.ScenarioMIP.MPI-M.MPI-ESM1-2-LR.ssp370.r1i1p1f1.fx.mrsofc.gn.v20190815",
        output_dir=tmpdir,
        output_type="nc",
        file_namer="standard",
        apply_fixes=False,
    )

    _check_output_nc(result, fname="mrsofc_fx_MPI-ESM1-2-LR_ssp370_r1i1p1f1_gn.nc")


# @pytest.mark.online
def test_subset_by_time_components_year_month(tmpdir, mini_esgf_data):
    tc1 = time_components(year=(2021, 2022), month=["dec", "jan", "feb"])
    tc2 = time_components(year=(2021, 2022), month=[12, 1, 2])

    for tc in (tc1, tc2):
        result = subset(
            mini_esgf_data["CMIP5_TAS_FPATH"],
            time_components=tc,
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )

        ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)

        assert set(ds.time.dt.year.values) == {2021, 2022}
        assert set(ds.time.dt.month.values) == {12, 1, 2}
        ds.close()


# @pytest.mark.online
def test_subset_by_time_components_month_day(tmpdir, mini_esgf_data):
    # 20051201-20151130
    tc1 = time_components(month=["jul"], day=[1, 11, 21])
    tc2 = time_components(month=[7], day=[1, 11, 21])

    for tc in (tc1, tc2):
        result = subset(
            mini_esgf_data["CMIP5_DAY"],
            time_components=tc,
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )

        ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)

        assert set(ds.time.dt.month.values) == {7}
        assert set(ds.time.dt.day.values) == {1, 11, 21}
        assert len(ds.time.values) == 30
        ds.close()


# @pytest.mark.online
def test_subset_by_time_interval_and_components_month_day(tmpdir, mini_esgf_data):
    # 20051201-20151130
    ys, ye = 2007, 2010
    ti = time_interval(f"{ys}-12-01T00:00:00", f"{ye}-11-30T23:59:59")

    months = [3, 4, 5]
    days = [5, 6]

    tc1 = time_components(month=["mar", "apr", "may"], day=days)
    tc2 = time_components(month=months, day=days)

    for tc in (tc1, tc2):
        result = subset(
            mini_esgf_data["CMIP5_DAY"],
            time=ti,
            time_components=tc,
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )
        ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)

        assert set(ds.time.dt.month.values) == set(months)
        assert set(ds.time.dt.day.values) == set(days)
        assert len(ds.time.values) == (ye - ys) * len(months) * len(days)
        ds.close()


# @pytest.mark.online
# def test_subset_by_time_series_and_components_month_day_cmip5(tmpdir, load_test_data):
#     # 20051201-20151130
#     ys, ye = 2007, 2010
#     req_times = [tm.isoformat() for tm in xr.open_dataset(CMIP5_DAY).time.values
#                  if ys <= tm.year <= ye]

#     ts = time_series(req_times)
#     months = [3, 4, 5]
#     days = [5, 6]

#     tc1 = time_components(month=["mar", "apr", "may"], day=days)
#     tc2 = time_components(month=months, day=days)

#     for tc in (tc1, tc2):
#         result = subset(
#             CMIP5_DAY, time=ts, time_components=tc, output_dir=tmpdir, file_namer="simple"
#         )
#         ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)

#         assert set(ds.time.dt.month.values) == set(months)
#         assert set(ds.time.dt.day.values) == set(days)
#         assert len(ds.time.values) == (ye - ys) * len(months) * len(days)
# dateutil.parser._parser.ParserError: day is out of range for month: 2007-02-29T12:00:00


# @pytest.mark.online
def test_subset_by_time_series_and_components_month_day_cmip6(tmpdir, mini_esgf_data):
    # 18500101-20141231

    # allow use of dataset - defaults to c3s-cmip6 and this is not in the catalog
    config_()["project:c3s-cmip6"]["use_catalog"] = False

    ys, ye = 1998, 2010
    req_times = [
        tm.isoformat()
        for tm in xr.open_dataset(mini_esgf_data["CMIP6_DAY"]).time.values
        if ys <= tm.year <= ye
    ]

    ts = time_series(req_times)
    months = [3, 4, 5]
    days = [5, 6]

    tc1 = time_components(month=["mar", "apr", "may"], day=days)
    tc2 = time_components(month=months, day=days)

    for tc in (tc1, tc2):
        result = subset(
            mini_esgf_data["CMIP6_DAY"],
            time=ts,
            time_components=tc,
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )
        ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)

        assert set(ds.time.dt.month.values) == set(months)
        assert set(ds.time.dt.day.values) == set(days)
        assert len(ds.time.values) == (ye - ys + 1) * len(months) * len(days)
        ds.close()


# @pytest.mark.online
def test_subset_components_day_monthly_dataset(tmpdir, mini_esgf_data):
    # tests key error is raised when trying to select a nonexistent day on a monthly dataset
    # 18500101-20141231

    # allow use of dataset - defaults to c3s-cmip6 and this is not in the catalog
    config_()["project:c3s-cmip6"]["use_catalog"] = False
    ys, ye = 1998, 2010
    req_times = [
        tm.isoformat()
        for tm in xr.open_dataset(mini_esgf_data["CMIP6_MONTH"]).time.values
        if ys <= tm.year <= ye
    ]

    ts = time_series(req_times)
    months = [3, 4, 5]
    days = [5, 6]

    tc = time_components(month=months, day=days)

    with pytest.raises(KeyError) as exc:
        subset(
            mini_esgf_data["CMIP6_MONTH"],
            time=ts,
            time_components=tc,
            output_dir=tmpdir,
            file_namer="simple",
            apply_fixes=False,
        )


# @pytest.mark.online
def test_subset_by_time_series(tmpdir, mini_esgf_data):
    t = [
        str(tm) for tm in xr.open_dataset(mini_esgf_data["CMIP5_TAS_FPATH"]).time.values
    ]
    some_times = [t[0], t[100], t[4], t[33], t[9]]

    result = subset(
        mini_esgf_data["CMIP5_TAS_FPATH"],
        time=time_series(some_times),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)

    ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)

    assert len(ds.time) == 5
    assert [str(t) for t in ds.time.values] == sorted(some_times)
    ds.tas.time.shape == (5,)

    ds.close()


# @pytest.mark.online
def test_subset_by_level_series(tmpdir, load_test_data):
    some_levels = [60000.0, 15000.0, 40000.0, 1000.0, 92500.0]

    result = subset(
        CMIP6_IDS[0],
        level=level_series(some_levels),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    _check_output_nc(result)

    ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)

    assert len(ds.plev) == 5
    np.testing.assert_array_equal(ds.plev.values, sorted(some_levels, reverse=True))
    ds.o3.plev.shape == (5,)

    ds.close()


# @pytest.mark.online
def test_subset_cmip6_nc_consistent_bounds(tmpdir, load_test_data):
    """Test daops subset to check consistent bounds in metadata."""
    result = subset(
        CMIP6_IDS[0],
        time=time_interval("1900-01-01T00:00:00", "1900-12-31T00:00:00"),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)
    # check fill value in bounds
    assert "_FillValue" not in ds.lat_bnds.encoding
    assert "_FillValue" not in ds.lon_bnds.encoding
    assert "_FillValue" not in ds.time_bnds.encoding
    # check fill value in coordinates
    assert "_FillValue" not in ds.time.encoding
    assert "_FillValue" not in ds.lat.encoding
    assert "_FillValue" not in ds.lon.encoding
    # assert "_FillValue" not in ds.height.encoding
    # check coordinates in bounds
    assert "coordinates" not in ds.lat_bnds.encoding
    assert "coordinates" not in ds.lon_bnds.encoding
    assert "coordinates" not in ds.time_bnds.encoding


# @pytest.mark.online
def test_subset_c3s_cmip6_nc_consistent_bounds(tmpdir, load_test_data):
    """Test daops subset to check consistent bounds in metadata."""
    result = subset(
        C3S_CMIP6_IDS[0],
        time=time_interval("2010-01-01T00:00:00", "2010-12-31T00:00:00"),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    ds = xr.open_dataset(result.file_uris[0], decode_times=TIME_CODER)
    # check fill value in bounds
    assert "_FillValue" not in ds.lat_bnds.encoding
    assert "_FillValue" not in ds.lon_bnds.encoding
    assert "_FillValue" not in ds.time_bnds.encoding
    # check fill value in coordinates
    assert "_FillValue" not in ds.time.encoding
    assert "_FillValue" not in ds.lat.encoding
    assert "_FillValue" not in ds.lon.encoding
    assert "_FillValue" not in ds.height.encoding
    # check coordinates in bounds
    assert "coordinates" not in ds.lat_bnds.encoding
    assert "coordinates" not in ds.lon_bnds.encoding
    assert "coordinates" not in ds.time_bnds.encoding
