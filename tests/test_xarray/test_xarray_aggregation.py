"""
test_xarray_aggregation.py
==========================

Set of tests to assert that Xarray behaves in ways we would expect when
it aggregates a time series of NetCDF files together into a single 
Dataset.

These tests use 3 NetCDF files (reduced sized), referenced by variables:
 - F1
 - F2
 - F3

"""

import itertools
import xarray as xr


test_files = [
    'path/to/tas...1950.nc',
    'path/to/tas...2000.nc',
    'path/to/tas...2050.nc'
]

#test_files = """/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r1i1p1/latest/tas/tas_day_HadGEM2-ES_rcp45_r1i1p1_20051201-20151130.nc
#/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r1i1p1/latest/tas/tas_day_HadGEM2-ES_rcp45_r1i1p1_20151201-20251130.nc
#/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r1i1p1/latest/tas/tas_day_HadGEM2-ES_rcp45_r1i1p1_20251201-20351130.nc""".split()

F1, F2, F3 = test_files


# Functions to make modified NC files

#TODO: Note, you might already have code elsewhere to modify files
# - if so, use that instead of defining functions here.

def _make_nc_modify_var_attr(nc_path, var_id, attr, value):
    # Maybe call NCO to generate the temporary file
    return tmp_path

def _make_nc_modify_global_attr(nc_path, attr, value):
    # Maybe call NCO to generate the temporary file
    return tmp_path

def _make_nc_modify_var_id(nc_path, old_var_id, new_var_id):
    # Maybe call NCO to generate the temporary file
    return tmp_path

def _make_nc_modify_fill_value(nc_path, var_id, fill_value=-1e20):
    # Maybe call NCO to generate the temporary file
    return tmp_path


def _open(file_paths):
    return xr.open_mfdataset(file_paths, use_cftime=True, combine='by_coords')
    

def test_agg_success_with_no_changes():
    ds = _open([F1, F2, F3])
    assert('tas' in ds.variables)


def test_agg_fails_diff_var_attrs():
    V = 'rubbish' 

    for attr, value in [('units', V), ('standard_name', V),
                        ('positive', V), ('long_name', V)]:
        file_paths = F1, _make_nc_modify_var_attr(F2, 'tas', attr, value), F3
        try:
            _open(file_paths)
        except ???
            assert(type of error and error string)

def test_agg_behaviour_diff_global_attrs():
    for gattr in ['product', 'source', 'institution', 'Conventions']:
        file_paths = F1, _make_nc_modify_global_attr(F2, gattr, 'other'), F3
        ds = _open(file_paths)
        assert(some sensible behaviour when aggregating global attrs - not sure what)


def test_agg_files_diff_var_id():
    file_paths = F1, _make_nc_modify_var_id(F2), F3
    try:
        _open(file_paths)
    except ???
        assert(type of error and error string)


def test_agg_fails_diff_fill_value():
    file_paths = F1, F2, _make_nc_modify_fill_value(F3, 'tas')
    try:
        _open(file_paths)
    except ???
        assert(type of error and error string)


def test_agg_failures_not_affected_by_order():
    # Apply a breaking change to different files in the sequence and
    # assert that the same exception is raised regardless of which 
    # file is modified
    file_orders = itertools.permutations([F1, F2, F3])
   
    for _f1, _f2, _f3 in file_orders:
        file_paths = _f1, _make_nc_modify_var_attr(_f2, 'tas', 'units', 'bad'), _f3
        try:
            _open(file_paths)
        except ???
            assert(type of error and error string)
    

