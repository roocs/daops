import pytest
import xarray as xr
import os

from daops.ops.subset import subset
from roocs_utils.exceptions import InvalidParameterValue, MissingParameterValue
from roocs_utils.parameter import (
    collection_parameter,
    area_parameter,
    time_parameter,
)

CMIP5_IDS = [
    "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas",
    "cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh",
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
    assert fname in [os.path.basename(_) for _ in result.file_paths]

# filename 'output.nc' comes from subset function in clisops repo
@pytest.mark.online
def test_subset_zostoga_with_fix(tmpdir):

    result = subset(
        CMIP5_IDS[0],
        time=("2085-01-16", "2120-12-16"),
        output_dir=tmpdir,
        file_namer="simple"
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
        file_namer="simple"
    )
    _check_output_nc(result)
    ds = xr.open_dataset(result.file_paths[0], use_cftime=True)
    assert ds.time.shape == (433,)


@pytest.mark.online
def test_subset_no_collection(tmpdir):
    with pytest.raises(TypeError):
        subset(
            time=("2085-01-16", "2120-12-16"),
            output_dir=tmpdir,
            file_namer="simple"
        )


@pytest.mark.online
def test_subset_collection_as_none(tmpdir):
    with pytest.raises(MissingParameterValue):
        subset(
            None,
            time=("2085-01-16", "2120-12-16"),
            output_dir=tmpdir,
            file_namer="simple"
        )


@pytest.mark.online
def test_subset_collection_as_empty_string(tmpdir):
    with pytest.raises(MissingParameterValue):
        subset(
            '',
            time=("2085-01-16", "2120-12-16"),
            output_dir=tmpdir,
            file_namer="simple"
        )


@pytest.mark.online
def test_subset_t_y_x(tmpdir):
    ds = xr.open_mfdataset(
        f"tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/"
        f"atmos/Amon/r1i1p1/latest/tas/*.nc", use_cftime=True, combine='by_coords'
    )
    assert ds.tas.shape == (3530, 2, 2)

    result = subset(
        CMIP5_IDS[1],
        time=("2085-01-16", "2120-12-16"),
        area=(0, -10, 120, 40),
        output_dir=tmpdir,
        file_namer="simple"
    )
    _check_output_nc(result)

    ds_subset = xr.open_dataset(result.file_paths[0], use_cftime=True)
    assert ds_subset.tas.shape == (433, 1, 1)


@pytest.mark.online
def test_subset_t_with_invalid_date(tmpdir):
    with pytest.raises(Exception) as exc:
        subset(
            CMIP5_IDS[1],
            time=("1985-01-16", "2002-12-16"),
            area=("0", "-10", "120", "40"),
            output_dir=tmpdir,
            file_namer="simple"
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
        file_namer="simple"
    )
    _check_output_nc(result)

    ds = xr.open_dataset(result.file_paths[0], use_cftime=True)
    assert ds.time.shape == (251,) or (252,)
    assert "lev" not in ds.dims  # checking that lev has been removed by fix
    ds.close()


@pytest.mark.online
def test_parameter_classes_as_args(tmpdir):
    collection = collection_parameter.CollectionParameter(CMIP5_IDS[1])
    time = time_parameter.TimeParameter(("2085-01-16", "2120-12-16"))
    area = area_parameter.AreaParameter((0, -10, 120, 40))

    result = subset(
            collection,
            time=time,
            area=area,
            output_dir=tmpdir,
            file_namer="simple"
        )
    _check_output_nc(result)

    ds_subset = xr.open_dataset(result.file_paths[0], use_cftime=True)
    assert ds_subset.tas.shape == (433, 1, 1)
