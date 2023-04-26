import pytest
import random
import xarray as xr
import os

from roocs_utils.xarray_utils.xarray_utils import open_xr_dataset

from daops.ops.subset import subset
from roocs_utils.parameter.param_utils import time_interval

from ._test_data_pools_example import data_pool_tests_db

from pdb import set_trace as ST


def _open_dataset(record):
    
    print(f'opening {record}')
    #====================================
    ## THIS OUGHT TO WORK, but I need to work out how to configure the paths
    ## for the tests.  strace shows that it is using /tmp/roocs.ini but this
    ## is overwritten every time (tests/conftest.py gets imported and
    ## write_roocs_cfg() is run)
    ##
    ## strace also says that it is also looking in all of these:
    ##     <roocs_dir>/clisops/clisops/etc/roocs.ini
    ##     <roocs_dir>/daops/daops/etc/roocs.ini
    ##     <roocs_dir>/roocs-utils/roocs_utils/etc/roocs.ini
    ##
    ## For now, symlinking ~/.mini-esgf-data/master/test_data/badc
    ## to point to the real /badc will do for a workaround -- now it finds 
    ## the dataset
    ds = open_xr_dataset(record)
    
    ## OR HERE IS ANOTHER POSSIBLE TEMPORARY WORKAROUND
    # import glob  # for open_xr_dataset workaround
    # assert isinstance(record, str)
    #paths = glob.glob(f'/badc/cmip6/data/{record.replace(".","/")}/*.nc')
    #ds = open_xr_dataset(paths)
    #====================================
    
    return ds


def _get_axes(ds):
    return {name: ds[name]  #getattr(ds, name)
            for name in ds.dims
            if name != 'bnds'}

def _rand_bool():
    return random.choice([True, False])

def _rand_nudge(axis, lower):
    if _rand_bool():
        return 0.
    size = len(axis)

    if lower == -1:
        lower = 0
    if lower == size - 1:
        lower = size - 2
    upper = lower + 1
    delta = axis[upper] - axis[lower]
    return delta * random.uniform(0.01, 0.99)

def _rand_nudge1():
    if _rand_bool():
        return 0.
    else:
        return random.uniform(0.01, 0.99)

def _get_rand_range(axis, max_length=5, do_nudge=False):
    """
    Returns a dictionary containing the (min, max) array values that can be used
    for subsetting and the subarray that would be expected to be produced by the
    subsettting.  It first chooses the index values that will be used, and then
    might randomly add some offset so that the actual requested min/max coordinate
    value is part way between that gridpoint and the next one - which should lead 
    to the same result in terms of which gridpoints are included in the subset.
    """
    size = len(axis)
    if size == 1:
        start = end = 0
        start_v = end_v = axis[0]
        if do_nudge:
            start_v -= _rand_nudge1()
            end_v -= _rand_nudge1()
    else:
        length = random.randint(1, min(size, max_length))
        start = random.randint(0, size - length - 1)
        end = length + start
        start_v = axis[start]
        end_v = axis[end]
        if do_nudge:
            start_v -= _rand_nudge(axis, start - 1)
            end_v += _rand_nudge(axis, end)

    return {'req_range': (start_v, end_v),
            'subarray': axis[start : end + 1]}


def _get_axis_by_direction(axes, direction):
    axes_in_dirn = [axis for axis in axes.values() if axis.axis == direction]
    axis, = axes_in_dirn  # assert size 1
    return axis

def _get_xaxis(axes): return _get_axis_by_direction(axes, 'X')
def _get_yaxis(axes): return _get_axis_by_direction(axes, 'Y')
def _get_zaxis(axes): return _get_axis_by_direction(axes, 'Z')
def _get_taxis(axes): return _get_axis_by_direction(axes, 'T')


def _get_rand_area(xaxis, yaxis):
    xrange = _get_rand_range(xaxis, do_nudge=True)
    yrange = _get_rand_range(yaxis, do_nudge=True)
    x1, x2 = [float(v) for v in xrange['req_range']]
    y1, y2 = sorted([float(v) for v in yrange['req_range']])
    return {'req_area': (x1, y1, x2, y2),
            'subarray_x': xrange['subarray'],
            'subarray_y': yrange['subarray']}


def _time_string(time_on_axis):
    t = time_on_axis.values.tolist()
    return (f'{t.year:04d}-{t.month:02d}-{t.day:02d}'
            f'T{t.hour:02d}:{t.minute:02d}:{t.second:02d}')
    

def _get_rand_time_int(taxis):
    trange = _get_rand_range(taxis, do_nudge=False)
    ts_start = _time_string(trange['req_range'][0])
    ts_end = _time_string(trange['req_range'][1])
    return {'req_interval': time_interval(ts_start, ts_end),
            'subarray': trange['subarray']}


def _prepare_test(ds, axes, do_area=False, do_time=False, do_levels=False):
    """
    returns the params to the subset function that will be needed for the test
    and a dictionary of things to expect to come back from the test
    """

    params = {}
    expect = {'axes': {}}

    raw_axes = []
    
    xaxis = _get_xaxis(axes)
    yaxis = _get_yaxis(axes)
    if do_area:
        area = _get_rand_area(xaxis, yaxis)
        params['area'] = area['req_area']
        expect['axes'][xaxis.name] = area['subarray_x']
        expect['axes'][yaxis.name] = area['subarray_y']
    else:
        raw_axes.extend([xaxis, yaxis])

    taxis = _get_taxis(axes)
    if do_time:
        interval = _get_rand_time_int(taxis)
        params['time'] = interval['req_interval']
        expect['axes'][taxis.name] = interval['subarray']
    else:
        raw_axes.append(taxis)

    for axis in raw_axes:
        expect['axes'][axis.name] = axis

        
    # TO DO: insert similar code for levels
        
    return params, expect


def _check_result(result, expect):

    fn, = result.file_uris
    os.system(f'ls -l {fn}')
    dsout = xr.open_dataset(fn)

    for axis_name, exp_axis in expect['axes'].items():
        print(f'checking {axis_name} axis values {exp_axis.values}')
        actual = dsout[axis_name]
        if not actual.equals(exp_axis):
            raise Exception(f'unexpected {axis_name} axis values, '
                            'expected {exp_axis.values} ,'
                            'got {actual.values}')

    # TO DO: TEST THAT AXES VALUES ARE COMPLETE SET?

    # TO DO: TEST DATA VALUES
        

def _cleanup(tmpdir, result):
    for path in result.file_uris:
        assert os.path.normpath(path).startswith(
                  os.path.normpath(f'{tmpdir}/'))
        print(f'deleting {path}')
        os.remove(path)
               
    
def _do_test(tmpdir, record, ds, axes, **kwargs):
    
    subset_params, expect = _prepare_test(ds, axes, **kwargs)

    print(f'\n\nDoing test with: params {subset_params}, writing to {tmpdir}')
    
    result = subset(record,
                    output_dir=tmpdir,
                    **subset_params)

    _check_result(result, expect)
    _cleanup(tmpdir, result)

    
@pytest.mark.parametrize("record", data_pool_tests_db)
def test_subset_in_data_pools(tmpdir, record):

    ds = _open_dataset(record)    
    axes = _get_axes(ds)

    # for now, one test: subset in area and time
    for _ in range(5):
        _do_test(tmpdir, record, ds, axes, do_area=True, do_time=True)

