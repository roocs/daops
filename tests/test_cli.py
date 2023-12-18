"""
Test the command line interface.

This module is based on test_subset.py, but the tests are made to use the CLI instead of
calling 'subset' directly.  String values are required by the CLI, and it is called
from a wrapper function is used that also expects string values, so the individual tests
are modified to allow for this.  Some tests have been removed where they are testing specific
input types.
"""

import os

import numpy as np
import pytest
import xarray as xr
import subprocess as sp
import py.path
import configparser
import tempfile

from daops import CONFIG
from tests._common import CMIP5_DAY
from tests._common import CMIP5_TAS_FPATH
from tests._common import CMIP6_DAY
from tests._common import CMIP6_MONTH
from tests._common import MINI_ESGF_MASTER_DIR

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
    assert fname in [os.path.basename(uri) for uri in result.file_uris]


def _commasep(lst):
    return ",".join(str(el) for el in lst)


def _time_components_str(**params):
    return "|".join(f"{k}:{_commasep(v)}" for k, v in params.items())


class _CliFail(Exception):
    pass


class _SimpleSubsetReturn:
    def __init__(self, file_uris):
        self.file_uris = file_uris


def _make_tmp_config(config_file, config_overrides):
    """
    Given a config file path and a list of (section, item, value) 3-tuples,
    create a temporary config file and return the path
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    for section, item, value in config_overrides:
        if not config.has_section(section):
            config.add_section(section)
        config[section][item] = str(value)

    with tempfile.NamedTemporaryFile(delete=False, mode="w+") as fout:
        tmp_config_file = fout.name
        config.write(fout)

    return tmp_config_file


def _cli_subset(*args, config_overrides=None, **kwargs):
    """
    A function that behaves somewhat similarly to calling subset directly,
    but instead wraps the CLI using subprocess.
    """

    config_env_var = "ROOCS_CONFIG"

    collections = args
    for c in collections:
        assert isinstance(c, str)

    mapping = {
        "time": "--time",
        "time_components": "--time-components",
        "area": "--area",
        "level": "--levels",
        "output_type": "--output-format",
        "output_dir": "--output-dir",
        "file_namer": "--file-namer",
    }

    cmdline = ["daops", "subset"]
    for k, v in kwargs.items():
        if isinstance(v, py.path.local):
            v = str(v)
        else:
            assert isinstance(v, str)
        # allow any unknown keys to raise exception
        cmdline.append(f"{mapping[k]}={v}")

    cmdline.extend(collections)

    if config_overrides:
        config_file = os.environ[config_env_var]
        tmp_config_file = _make_tmp_config(config_file, config_overrides)
        os.environ[config_env_var] = tmp_config_file

    proc = sp.Popen(cmdline, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = proc.communicate()

    if config_overrides:
        os.remove(tmp_config_file)
        os.environ[config_env_var] = config_file

    if proc.returncode != 0:
        msg = f"""CLI Failed:
cmdline: {" ".join(cmdline)}
status code: {proc.returncode}
stdout: {stdout}
stderr: {stderr}"""
        raise _CliFail(msg)

    file_uris = [line.strip() for line in stdout.decode().strip().split("\n")]
    return _SimpleSubsetReturn(file_uris)


@pytest.mark.online
def test_cli_subset_zostoga(tmpdir, load_esgf_test_data):
    result = _cli_subset(
        CMIP5_IDS[0],
        time="2085-01-16/2120-12-16",
        output_dir=tmpdir,
        file_namer="simple",
    )

    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)
    assert ds.time.shape == (192,)

    # lev should still be in ds.dims because fix hasn't been applied
    assert "lev" in ds.dims


@pytest.mark.online
def test_cli_subset_t(tmpdir, load_esgf_test_data):
    result = _cli_subset(
        CMIP5_IDS[1],
        time="2085-01-16/2120-12-16",
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)
    assert ds.time.shape == (433,)


@pytest.mark.online
def test_cli_subset_collection_as_empty_string(tmpdir):
    with pytest.raises(_CliFail):
        _cli_subset(
            "",
            time="2085-01-16/2120-12-16",
            output_dir=tmpdir,
            file_namer="simple",
        )


@pytest.mark.online
def test_cli_subset_t_y_x(tmpdir, load_esgf_test_data):
    fpath = (
        f"{MINI_ESGF_MASTER_DIR}/"
        "test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/"
        "atmos/Amon/r1i1p1/latest/tas/*.nc"
    )

    ds = xr.open_mfdataset(
        fpath,
        use_cftime=True,
        combine="by_coords",
    )
    assert ds.tas.shape == (3530, 2, 2)

    result = _cli_subset(
        CMIP5_IDS[1],
        time="2085-01-16/2120-12-16",
        area="0,-10,120,40",
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)

    ds_subset = xr.open_dataset(result.file_uris[0], use_cftime=True)
    assert ds_subset.tas.shape == (433, 1, 1)


@pytest.mark.online
def test_cli_subset_t_z_y_x(tmpdir, load_esgf_test_data):
    fpath = (
        f"{MINI_ESGF_MASTER_DIR}/"
        "test_data/badc/cmip6/data/CMIP6/CMIP/NOAA-GFDL/"
        "GFDL-ESM4/historical/r1i1p1f1/Amon/o3/gr1/v20190726/"
        "o3_Amon_GFDL-ESM4_historical_r1i1p1f1_gr1_185001-194912.nc"
    )

    ds = xr.open_mfdataset(
        fpath,
        use_cftime=True,
        combine="by_coords",
    )

    assert ds.o3.shape == (1200, 19, 2, 3)
    assert list(ds.o3.coords["plev"].values) == [
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
    ]

    result = _cli_subset(
        CMIP6_IDS[0],
        time="1900-01-16/1900-12-16",
        area="0,-10,120,40",
        level="10000/850.0",
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)

    ds_subset = xr.open_dataset(result.file_uris[0], use_cftime=True)
    assert ds_subset.o3.shape == (12, 6, 1, 1)


@pytest.mark.online
def test_cli_subset_t_with_invalid_date(tmpdir, load_esgf_test_data):
    with pytest.raises(_CliFail) as exc:
        _cli_subset(
            CMIP5_IDS[1],
            time="1985-01-16/2002-12-16",
            area="0,-10,120,40",
            output_dir=tmpdir,
            file_namer="simple",
        )
    assert (
        "No files found in given time range for "
        "cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas"
        in str(exc.value)
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
def test_time_is_none(tmpdir, load_esgf_test_data):
    result = _cli_subset(
        CMIP5_IDS[1],
        area="0,-10,120,40",
        output_dir=tmpdir,
        file_namer="simple",
    )

    _check_output_nc(result)

    ds = xr.open_mfdataset(
        os.path.join(
            CONFIG["project:cmip5"]["base_dir"],
            "output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        ),
        use_cftime=True,
    )
    ds_subset = xr.open_dataset(result.file_uris[0], use_cftime=True)

    assert ds_subset.time.values.min().strftime(
        "%Y-%m-%d"
    ) == ds.time.values.min().strftime("%Y-%m-%d")
    assert ds_subset.time.values.max().strftime(
        "%Y-%m-%d"
    ) == ds.time.values.max().strftime("%Y-%m-%d")


@pytest.mark.online
def test_end_time_is_none(tmpdir, load_esgf_test_data):
    result = _cli_subset(
        CMIP5_IDS[2],
        time="1940-10-14/",
        area="0,-10,120,40",
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)

    ds = xr.open_mfdataset(
        os.path.join(
            CONFIG["project:cmip5"]["base_dir"],
            "output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/latest/rh/*.nc",
        ),
        use_cftime=True,
    )
    ds_subset = xr.open_dataset(result.file_uris[0], use_cftime=True)

    assert ds_subset.time.values.min().strftime("%Y-%m-%d") == "1940-10-16"
    assert ds_subset.time.values.max().strftime(
        "%Y-%m-%d"
    ) == ds.time.values.max().strftime("%Y-%m-%d")


@pytest.mark.online
def test_start_time_is_none(tmpdir, load_esgf_test_data):
    result = _cli_subset(
        CMIP5_IDS[1],
        time="/2120-12-16",
        area="0,-10,120,40",
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)

    ds = xr.open_mfdataset(
        os.path.join(
            CONFIG["project:cmip5"]["base_dir"],
            "output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        ),
        use_cftime=True,
    )
    ds_subset = xr.open_dataset(result.file_uris[0], use_cftime=True)

    assert ds_subset.time.values.min().strftime(
        "%Y-%m-%d"
    ) == ds.time.values.min().strftime("%Y-%m-%d")
    assert ds_subset.time.values.max().strftime("%Y-%m-%d") == "2120-12-16"


@pytest.mark.online
def test_time_invariant_subset_standard_name(tmpdir, load_esgf_test_data):
    dset = "CMIP6.ScenarioMIP.IPSL.IPSL-CM6A-LR.ssp119.r1i1p1f1.fx.mrsofc.gr.v20190410"

    result = _cli_subset(
        dset,
        area="5.0,10.0,300.0,80.0",
        output_dir=tmpdir,
        output_type="nc",
        file_namer="standard",
    )

    assert "mrsofc_fx_IPSL-CM6A-LR_ssp119_r1i1p1f1_gr.nc" in result.file_uris[0]


@pytest.mark.online
def test_cli_subset_with_multiple_collections(tmpdir, load_esgf_test_data):
    file_paths = [
        f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES"
        f"/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_200512-203011.nc",
        f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES"
        f"/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_203012-205511.nc",
    ]

    result = _cli_subset(
        *file_paths,
        time="2008-01-16/2028-12-16",
        output_dir=tmpdir,
        output_type="nc",
        file_namer="standard",
    )

    assert "tas_mon_HadGEM2-ES_rcp85_r1i1p1_20080116-20281216.nc" in result.file_uris[0]


@pytest.mark.online
def test_cli_subset_with_catalog(tmpdir, load_esgf_test_data):
    # c3s-cmip6 dataset so will use catalog in consolidate
    result = _cli_subset(
        "c3s-cmip6.ScenarioMIP.INM.INM-CM5-0.ssp245.r1i1p1f1.Amon.rlds.gr1.v20190619",
        time="2028-01-16/2050-12-16",
        output_dir=tmpdir,
        output_type="nc",
        file_namer="standard",
    )

    _check_output_nc(
        result, fname="rlds_Amon_INM-CM5-0_ssp245_r1i1p1f1_gr1_20280116-20501216.nc"
    )


@pytest.mark.online
def test_cli_subset_with_catalog_time_invariant(tmpdir, load_esgf_test_data):
    # c3s-cmip6 dataset so will use catalog in consolidate
    result = _cli_subset(
        f"c3s-cmip6.ScenarioMIP.MPI-M.MPI-ESM1-2-LR.ssp370.r1i1p1f1.fx.mrsofc.gn.v20190815",
        output_dir=tmpdir,
        output_type="nc",
        file_namer="standard",
    )

    _check_output_nc(result, fname="mrsofc_fx_MPI-ESM1-2-LR_ssp370_r1i1p1f1_gn.nc")


@pytest.mark.online
def test_cli_subset_by_time_components_year_month(tmpdir, load_esgf_test_data):
    tc1 = _time_components_str(year=(2021, 2022), month=["dec", "jan", "feb"])
    tc2 = _time_components_str(year=(2021, 2022), month=[12, 1, 2])

    for tc in (tc1, tc2):
        result = _cli_subset(
            CMIP5_TAS_FPATH, time_components=tc, output_dir=tmpdir, file_namer="simple"
        )

        ds = xr.open_dataset(result.file_uris[0], use_cftime=True)

        assert set(ds.time.dt.year.values) == {2021, 2022}
        assert set(ds.time.dt.month.values) == {12, 1, 2}
        ds.close()


@pytest.mark.online
def test_cli_subset_by_time_components_month_day(tmpdir, load_esgf_test_data):
    # 20051201-20151130
    tc1 = _time_components_str(month=["jul"], day=[1, 11, 21])
    tc2 = _time_components_str(month=[7], day=[1, 11, 21])

    for tc in (tc1, tc2):
        result = _cli_subset(
            CMIP5_DAY, time_components=tc, output_dir=tmpdir, file_namer="simple"
        )

        ds = xr.open_dataset(result.file_uris[0], use_cftime=True)

        assert set(ds.time.dt.month.values) == {7}
        assert set(ds.time.dt.day.values) == {1, 11, 21}
        assert len(ds.time.values) == 30
        ds.close()


@pytest.mark.online
def test_cli_subset_by_time_interval_and_components_month_day(
    tmpdir, load_esgf_test_data
):
    # 20051201-20151130
    ys, ye = 2007, 2010
    ti = f"{ys}-12-01T00:00:00/{ye}-11-30T23:59:59"

    months = [3, 4, 5]
    days = [5, 6]

    tc1 = _time_components_str(month=["mar", "apr", "may"], day=days)
    tc2 = _time_components_str(month=months, day=days)

    for tc in (tc1, tc2):
        result = _cli_subset(
            CMIP5_DAY,
            time=ti,
            time_components=tc,
            output_dir=tmpdir,
            file_namer="simple",
        )
        ds = xr.open_dataset(result.file_uris[0], use_cftime=True)

        assert set(ds.time.dt.month.values) == set(months)
        assert set(ds.time.dt.day.values) == set(days)
        assert len(ds.time.values) == (ye - ys) * len(months) * len(days)
        ds.close()


# @pytest.mark.online
# def test_cli_subset_by_time_series_and_components_month_day_cmip5(tmpdir, load_esgf_test_data):
#     # 20051201-20151130
#     ys, ye = 2007, 2010
#     req_times = [tm.isoformat() for tm in xr.open_dataset(CMIP5_DAY).time.values
#                  if ys <= tm.year <= ye]

#     ts = ",".join(req_times)
#     months = [3, 4, 5]
#     days = [5, 6]

#     tc1 = _time_components_str(month=["mar", "apr", "may"], day=days)
#     tc2 = _time_components_str(month=months, day=days)

#     for tc in (tc1, tc2):
#         result = _cli_subset(
#             CMIP5_DAY, time=ts, _time_components_str=tc, output_dir=tmpdir, file_namer="simple"
#         )
#         ds = xr.open_dataset(result.file_uris[0], use_cftime=True)

#         assert set(ds.time.dt.month.values) == set(months)
#         assert set(ds.time.dt.day.values) == set(days)
#         assert len(ds.time.values) == (ye - ys) * len(months) * len(days)
# dateutil.parser._parser.ParserError: day is out of range for month: 2007-02-29T12:00:00


@pytest.mark.online
def test_cli_subset_by_time_series_and_components_month_day_cmip6(
    tmpdir, load_esgf_test_data
):
    # 18500101-20141231

    # allow use of dataset - defaults to c3s-cmip6 and this is not in the catalog
    config_overrides = [
        ("project:c3s-cmip6", "use_catalog", False),
    ]

    ys, ye = 1998, 2010
    req_times = [
        tm.isoformat()
        for tm in xr.open_dataset(CMIP6_DAY).time.values
        if ys <= tm.year <= ye
    ]

    ts = ",".join(req_times)
    months = [3, 4, 5]
    days = [5, 6]

    tc1 = _time_components_str(month=["mar", "apr", "may"], day=days)
    tc2 = _time_components_str(month=months, day=days)

    for tc in (tc1, tc2):
        result = _cli_subset(
            CMIP6_DAY,
            time=ts,
            time_components=tc,
            output_dir=tmpdir,
            file_namer="simple",
            config_overrides=config_overrides,
        )
        ds = xr.open_dataset(result.file_uris[0], use_cftime=True)

        assert set(ds.time.dt.month.values) == set(months)
        assert set(ds.time.dt.day.values) == set(days)
        assert len(ds.time.values) == (ye - ys + 1) * len(months) * len(days)
        ds.close()


@pytest.mark.online
def test_cli_subset_components_day_monthly_dataset(tmpdir, load_esgf_test_data):
    #  tests key error is raised when trying to select a non existent day on a monthly dataset
    # 18500101-20141231

    # allow use of dataset - defaults to c3s-cmip6 and this is not in the catalog
    CONFIG["project:c3s-cmip6"]["use_catalog"] = False
    ys, ye = 1998, 2010
    req_times = [
        tm.isoformat()
        for tm in xr.open_dataset(CMIP6_MONTH).time.values
        if ys <= tm.year <= ye
    ]

    ts = ",".join(req_times)
    months = [3, 4, 5]
    days = [5, 6]

    tc = _time_components_str(month=months, day=days)

    with pytest.raises(_CliFail) as exc:
        _cli_subset(
            CMIP6_MONTH,
            time=ts,
            time_components=tc,
            output_dir=tmpdir,
            file_namer="simple",
        )


@pytest.mark.online
def test_cli_subset_by_time_series(tmpdir, load_esgf_test_data):
    t = [str(tm) for tm in xr.open_dataset(CMIP5_TAS_FPATH).time.values]
    some_times = [t[0], t[100], t[4], t[33], t[9]]

    result = _cli_subset(
        CMIP5_TAS_FPATH,
        time=",".join(some_times),
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)

    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)

    assert len(ds.time) == 5
    assert [str(t) for t in ds.time.values] == sorted(some_times)
    ds.tas.time.shape == (5,)

    ds.close()


@pytest.mark.online
def test_cli_subset_by_level_series(tmpdir, load_esgf_test_data):
    some_levels = [60000.0, 15000.0, 40000.0, 1000.0, 92500.0]

    result = _cli_subset(
        CMIP6_IDS[0],
        level=",".join(str(lev) for lev in some_levels),
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)

    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)

    assert len(ds.plev) == 5
    np.testing.assert_array_equal(ds.plev.values, sorted(some_levels, reverse=True))
    ds.o3.plev.shape == (5,)

    ds.close()


@pytest.mark.online
def test_cli_subset_cmip6_nc_consistent_bounds(tmpdir, load_esgf_test_data):
    """Test daops subset to check consistent bounds in metadata."""
    result = _cli_subset(
        CMIP6_IDS[0],
        time="1900-01-01T00:00:00/1900-12-31T00:00:00",
        output_dir=tmpdir,
        file_namer="simple",
    )
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)
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


@pytest.mark.online
def test_cli_subset_c3s_cmip6_nc_consistent_bounds(tmpdir, load_esgf_test_data):
    """Test daops subset to check consistent bounds in metadata."""
    result = _cli_subset(
        C3S_CMIP6_IDS[0],
        time="2010-01-01T00:00:00/2010-12-31T00:00:00",
        output_dir=tmpdir,
        file_namer="simple",
    )
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)
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
