import os

import pytest
import xarray as xr
from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.exceptions import MissingParameterValue
from roocs_utils.parameter import area_parameter
from roocs_utils.parameter import collection_parameter
from roocs_utils.parameter import time_parameter

from daops import CONFIG
from daops.ops.subset import subset

CMIP5_IDS = [
    "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas",
    "cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh",
]

CMIP6_IDS = ["CMIP6.CMIP.NOAA-GFDL.GFDL-ESM4.historical.r1i1p1f1.Amon.o3.gr1.v20190726"]

zostoga_ids = [
    "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.BCC.bcc-csm1-1.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MOHC.HadGEM2-ES.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.CCCma.CanCM4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.IPSL.IPSL-CM5A-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
]


def _check_output_nc(result, fname="output_001.nc"):
    assert fname in [os.path.basename(_) for _ in result.file_paths]


# filename 'output.nc' comes from subset function in clisops repo
@pytest.mark.online
def test_subset_zostoga_with_fix(tmpdir):

    result = subset(
        CMIP5_IDS[0],
        time=("2085-01-16", "2120-12-16"),
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_paths[0], use_cftime=True)
    assert ds.time.shape == (192,)
    assert "lev" not in ds.dims


@pytest.mark.online
def test_subset_t(tmpdir):
    result = subset(
        CMIP5_IDS[1],
        time=("2085-01-16", "2120-12-16"),
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_paths[0], use_cftime=True)
    assert ds.time.shape == (433,)


@pytest.mark.online
def test_subset_no_collection(tmpdir):
    with pytest.raises(TypeError):
        subset(
            time=("2085-01-16", "2120-12-16"), output_dir=tmpdir, file_namer="simple"
        )


@pytest.mark.online
def test_subset_collection_as_none(tmpdir):
    with pytest.raises(MissingParameterValue):
        subset(
            None,
            time=("2085-01-16", "2120-12-16"),
            output_dir=tmpdir,
            file_namer="simple",
        )


@pytest.mark.online
def test_subset_collection_as_empty_string(tmpdir):
    with pytest.raises(MissingParameterValue):
        subset(
            "",
            time=("2085-01-16", "2120-12-16"),
            output_dir=tmpdir,
            file_namer="simple",
        )


@pytest.mark.online
def test_subset_t_y_x(tmpdir):
    ds = xr.open_mfdataset(
        f"tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/"
        f"atmos/Amon/r1i1p1/latest/tas/*.nc",
        use_cftime=True,
        combine="by_coords",
    )
    assert ds.tas.shape == (3530, 2, 2)

    result = subset(
        CMIP5_IDS[1],
        time=("2085-01-16", "2120-12-16"),
        area=(0, -10, 120, 40),
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)

    ds_subset = xr.open_dataset(result.file_paths[0], use_cftime=True)
    assert ds_subset.tas.shape == (433, 1, 1)


@pytest.mark.online
def test_subset_t_z_y_x(tmpdir):
    ds = xr.open_mfdataset(
        "tests/mini-esgf-data/test_data/badc/cmip6/data/CMIP6/CMIP/NOAA-GFDL/"
        "GFDL-ESM4/historical/r1i1p1f1/Amon/o3/gr1/v20190726/"
        "o3_Amon_GFDL-ESM4_historical_r1i1p1f1_gr1_185001-194912.nc",
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

    result = subset(
        CMIP6_IDS[0],
        time=("1890-01-16", "1901-12-16"),
        area=(0, -10, 120, 40),
        level=(10000, 850.0),
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)

    ds_subset = xr.open_dataset(result.file_paths[0], use_cftime=True)
    assert ds_subset.o3.shape == (143, 6, 1, 1)


@pytest.mark.online
def test_subset_t_with_invalid_date(tmpdir):
    with pytest.raises(Exception) as exc:
        subset(
            CMIP5_IDS[1],
            time=("1985-01-16", "2002-12-16"),
            area=("0", "-10", "120", "40"),
            output_dir=tmpdir,
            file_namer="simple",
        )
        assert (
            exc.value == "No files found in given time range for "
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
        time=("2008-01-16", "2028-12-16"),
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)

    ds = xr.open_dataset(result.file_paths[0], use_cftime=True)
    assert ds.time.shape in [(251,), (252,)]
    assert "lev" not in ds.dims  # checking that lev has been removed by fix
    ds.close()


@pytest.mark.online
def test_parameter_classes_as_args(tmpdir):
    collection = collection_parameter.CollectionParameter(CMIP5_IDS[1])
    time = time_parameter.TimeParameter(("2085-01-16", "2120-12-16"))
    area = area_parameter.AreaParameter((0, -10, 120, 40))

    result = subset(
        collection, time=time, area=area, output_dir=tmpdir, file_namer="simple"
    )
    _check_output_nc(result)

    ds_subset = xr.open_dataset(result.file_paths[0], use_cftime=True)
    assert ds_subset.tas.shape == (433, 1, 1)


@pytest.mark.online
def test_time_is_none(tmpdir):

    result = subset(
        CMIP5_IDS[1],
        time=None,
        area=("0", "-10", "120", "40"),
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)

    ds = xr.open_mfdataset(
        os.path.join(
            CONFIG["project:cmip5"]["base_dir"],
            "cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        ),
        use_cftime=True,
    )
    ds_subset = xr.open_dataset(result.file_paths[0], use_cftime=True)

    assert ds_subset.time.values.min().strftime(
        "%Y-%m-%d"
    ) == ds.time.values.min().strftime("%Y-%m-%d")
    assert ds_subset.time.values.max().strftime(
        "%Y-%m-%d"
    ) == ds.time.values.max().strftime("%Y-%m-%d")


@pytest.mark.online
def test_end_time_is_none(tmpdir):

    result = subset(
        CMIP5_IDS[2],
        time="1940-10-14/",
        area=("0", "-10", "120", "40"),
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)

    ds = xr.open_mfdataset(
        os.path.join(
            CONFIG["project:cmip5"]["base_dir"],
            "cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/latest/rh/*.nc",
        ),
        use_cftime=True,
    )
    ds_subset = xr.open_dataset(result.file_paths[0], use_cftime=True)

    assert ds_subset.time.values.min().strftime("%Y-%m-%d") == "1940-10-16"
    assert ds_subset.time.values.max().strftime(
        "%Y-%m-%d"
    ) == ds.time.values.max().strftime("%Y-%m-%d")


@pytest.mark.online
def test_start_time_is_none(tmpdir):

    result = subset(
        CMIP5_IDS[1],
        time="/2120-12-16",
        area=("0", "-10", "120", "40"),
        output_dir=tmpdir,
        file_namer="simple",
    )
    _check_output_nc(result)

    ds = xr.open_mfdataset(
        os.path.join(
            CONFIG["project:cmip5"]["base_dir"],
            "cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        ),
        use_cftime=True,
    )
    ds_subset = xr.open_dataset(result.file_paths[0], use_cftime=True)

    assert ds_subset.time.values.min().strftime(
        "%Y-%m-%d"
    ) == ds.time.values.min().strftime("%Y-%m-%d")
    assert ds_subset.time.values.max().strftime("%Y-%m-%d") == "2120-12-16"
