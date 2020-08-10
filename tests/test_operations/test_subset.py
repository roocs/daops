import pytest
import xarray as xr

from daops.ops.subset import subset
from daops import options
from tests._common import get_tests_project_base_dir
from unittest import mock
from unittest.mock import Mock

CMIP5_IDS = [
    'cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga',
    'cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas',
    'cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh'
]

zostoga_ids = ["cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
               "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
               "cmip5.output1.BCC.bcc-csm1-1.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
               "cmip5.output1.MOHC.HadGEM2-ES.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
               "cmip5.output1.CCCma.CanCM4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
               "cmip5.output1.IPSL.IPSL-CM5A-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
               ]


# filename 'output.nc' comes from subset function in clisops repo 
@pytest.mark.online
@mock.patch('daops.ops.subset.get_project_base_dir', side_effect=get_tests_project_base_dir)
def test_subset_zostoga_with_fix(mock_dirs):

    result = subset(CMIP5_IDS[0],
                    project='cmip5',
                    time=('2085-01-01', '2120-12-30'),
                    output_dir='outputs')
    assert result.file_paths == ['outputs/output.nc']
    ds = xr.open_dataset('outputs/output.nc')
    assert ds.time.shape == (192,)
    assert 'lev' not in ds.dims


@pytest.mark.online
@mock.patch('daops.ops.subset.get_project_base_dir', side_effect=get_tests_project_base_dir)
def test_subset_t(mock_dirs):
    result = subset(CMIP5_IDS[1],
                    project='cmip5',
                    time=('2085-01-01', '2120-12-30'),
                    output_dir='outputs')
    assert result.file_paths == ['outputs/output.nc']
    ds = xr.open_dataset('outputs/output.nc')
    assert ds.time.shape == (433,)


@pytest.mark.online
@mock.patch('daops.ops.subset.get_project_base_dir', side_effect=get_tests_project_base_dir)
def test_subset_t_y_x(mock_dirs):
    ds = xr.open_mfdataset(f'tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/'
                           f'atmos/Amon/r1i1p1/latest/tas/*.nc')
    assert ds.tas.shape == (3530, 2, 2)

    result = subset(CMIP5_IDS[1],
                    project='cmip5',
                    time=('2085-01-01', '2120-12-30'),
                    space=('0', '-10', '120', '40'),
                    output_dir='outputs')
    assert result.file_paths == ['outputs/output.nc']

    ds_subset = xr.open_dataset('outputs/output.nc')
    assert ds_subset.tas.shape == (433, 1, 1)


@pytest.mark.online
@mock.patch('daops.ops.subset.get_project_base_dir', side_effect=get_tests_project_base_dir)
def test_subset_t_with_invalid_date(mock_dirs):
    with pytest.raises(Exception) as exc:
        subset(CMIP5_IDS[1],
               project='cmip5',
               time=('1985-01-01', '2002-12-31'),
               output_dir='outputs')
        assert exc.value == "No files found in given time range"


@pytest.fixture(params=[zostoga_ids[0], zostoga_ids[1], zostoga_ids[2], zostoga_ids[3], zostoga_ids[4], zostoga_ids[5]])
def zostoga_id(request):
    id = request.param
    return id


@pytest.mark.online
@mock.patch('daops.ops.subset.get_project_base_dir', side_effect=get_tests_project_base_dir)
def test_subset_with_fix_and_multiple_ids(mock_dirs, zostoga_id):
    
    result = subset(zostoga_id,
                    project='cmip5',
                    time=('2008-01-01', '2028-12-30'),
                    output_dir='outputs')
    assert result.file_paths == ['outputs/output.nc']

    ds = xr.open_dataset('outputs/output.nc')
    assert ds.time.shape == (252,) # all datasets have the same time shape
    assert 'lev' not in ds.dims # checking that lev has been removed by fix
    ds.close()



