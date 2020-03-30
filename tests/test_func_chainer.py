from daops import utils
from ._common import CMIP5_ARCHIVE_BASE

import xarray as xr

CMIP5_IDS = [
    'cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga',
    'cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas',
    'cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh'
]


# setup for tests
def setup_module(module):
    module.CMIP5_ARCHIVE_BASE = 'tests/mini-esgf-data/test_data/badc/cmip5/data'
    utils.fixer.Fixer.FIX_DIR = 'tests/test_fixes'
    module.CMIP5_FPATHS = [
        CMIP5_ARCHIVE_BASE + '/cmip5/output1/INM/inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc',
        CMIP5_ARCHIVE_BASE + '/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc',
        CMIP5_ARCHIVE_BASE + '/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/latest/rh/*.nc'
    ]


def test_pre_and_post_process_fix():
    ds_test = xr.open_mfdataset(CMIP5_FPATHS[1])
    ds_test['tas'].data = ds_test['tas'].data * 2
    ds_test['tas'].data = ds_test['tas'].data + 100
    ds_code = utils.core.open_dataset(CMIP5_IDS[1], CMIP5_FPATHS[1])
    assert (ds_test.tas.values == ds_code.tas.values).all


def test_post_process_fix_only():
    ds_test = xr.open_mfdataset(CMIP5_FPATHS[0])
    ds_test['zostoga'].attrs['units'] = 's'
    ds_test['zostoga'].attrs['long_name'] = 'silly'
    ds_code = utils.core.open_dataset(CMIP5_IDS[0], CMIP5_FPATHS[0])
    assert ds_test['zostoga'].units == ds_code['zostoga'].units
    assert ds_test['zostoga'].long_name == ds_code['zostoga'].long_name


def test_pre_process_fix_only():
    ds = xr.open_mfdataset(CMIP5_FPATHS[2])
    ds_test = ds.rename({'lat': 'silly_lat'})
    ds_code = utils.core.open_dataset(CMIP5_IDS[2], CMIP5_FPATHS[2])
    assert ds_test.dims == ds_code.dims


def teardown_module(module):
    module.CMIP5_ARCHIVE_BASE = 'tests/mini-esgf-data/test_data/badc/cmip5/data'
    utils.fixer.Fixer.FIX_DIR  = 'tests/test_fixes'
    module.CMIP5_FPATHS = [
        CMIP5_ARCHIVE_BASE + '/cmip5/output1/INM/inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc',
        CMIP5_ARCHIVE_BASE + '/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc',
        CMIP5_ARCHIVE_BASE + '/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/latest/rh/*.nc'
    ]
