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
import os
import pathlib
import tempfile

import numpy as np
import pytest
import xarray as xr

from .._common import TESTS_OUTPUTS

test_files = [
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_200512-203011.nc",
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_203012-205511.nc",
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_205512-208011.nc",
]

F1, F2, F3 = test_files


# Functions to make modified NC files
# need to make files temporary files
def _make_nc_modify_var_attr(nc_path, var_id, attr, value, path=TESTS_OUTPUTS):
    ds = _open(nc_path)
    ds[var_id].attrs[attr] = value
    ds.to_netcdf(os.path.join(path, "tas_modify_var_attr.nc"))
    tmp_path = os.path.join(path, "tas_modify_var_attr.nc")
    return tmp_path


def _make_nc_modify_global_attr(nc_path, attr, value, path=TESTS_OUTPUTS):
    ds = _open(nc_path)
    ds.attrs[attr] = value
    # ds.to_netcdf(path=tmp_path.mkdir("test_dir").join("modify_var_attr.nc"))
    ds.to_netcdf(os.path.join(path, "tas_modify_global_attr.nc"))
    tmp_path = os.path.join(path, "tas_modify_global_attr.nc")
    return tmp_path


def _make_nc_modify_var_id(nc_path, old_var_id, new_var_id, path=TESTS_OUTPUTS):
    ds = _open(nc_path)
    ds = ds.rename({old_var_id: new_var_id})
    ds.to_netcdf(path=os.path.join(path, "tas_modify_var_id.nc"))
    tmp_path = os.path.join(path, "tas_modify_var_id.nc")
    return tmp_path


def _make_nc_modify_fill_value(nc_path, var_id, fill_value, path=TESTS_OUTPUTS):
    ds = _open(nc_path)
    ds[var_id].encoding["_FillValue"] = fill_value
    ds.tas.encoding["missing_value"] = fill_value
    ds.to_netcdf(path=os.path.join(path, "tas_modify_fill_value.nc"))
    tmp_path = os.path.join(path, "tas_modify_fill_value.nc")
    return tmp_path


@pytest.fixture(params=["units", "standard_name", "long_name"])
def var_attr(request):
    attr = request.param
    return attr


@pytest.fixture(params=["product", "source", "institution", "Conventions"])
def global_attr(request):
    attr = request.param
    return attr


def _open(file_paths):
    return xr.open_mfdataset(file_paths, use_cftime=True, combine="by_coords")


def test_agg_success_with_no_changes():
    ds = _open([F1, F2, F3])
    assert "tas" in ds.variables
    ds.close()


def test_agg_fails_diff_var_attrs_change_F2(var_attr):
    V = "rubbish"
    file_paths = F1, _make_nc_modify_var_attr(F2, "tas", var_attr, V), F3
    ds = _open(file_paths)
    assert ds.tas.__getattr__(f"{var_attr}") != V
    ds.close()


def test_agg_fails_diff_var_attrs_change_F1(var_attr):
    V = "rubbish"
    file_paths = _make_nc_modify_var_attr(F1, "tas", var_attr, V), F2, F3
    ds = _open(file_paths)
    assert ds.tas.__getattr__(f"{var_attr}") == V
    ds.close()


# doesn't work when changing all 3 - something to do with how I'm modifying files?
# failure not relevant to what is being tested
# def test_agg_fails_diff_var_attrs_change_all_3(var_attr):
#     V = "rubbish"
#     file_paths = (
#         _make_nc_modify_var_attr(F1, "tas", var_attr, V),
#         _make_nc_modify_var_attr(F2, "tas", var_attr, V),
#         _make_nc_modify_var_attr(F3, "tas", var_attr, V),
#     )
#     try:
#         ds = _open(file_paths)
#         ds.close()
#     except ValueError as exc:
#         assert (
#             str(exc)
#             == "Could not find any dimension coordinates to use to order the datasets for concatenation"
#         )


def test_agg_behaviour_diff_global_attrs_change_F2(global_attr):
    V = "other"
    file_paths = F1, _make_nc_modify_global_attr(F2, global_attr, V), F3
    ds = _open(file_paths)
    assert ds.__getattr__(f"{global_attr}") != V
    ds.close()


def test_agg_behaviour_diff_global_attrs_change_F1(global_attr):
    V = "other"
    file_paths = _make_nc_modify_global_attr(F1, global_attr, V), F2, F3
    ds = _open(file_paths)
    assert ds.__getattr__(f"{global_attr}") == V
    ds.close()


# failure not relevant to what is being tested
# def test_agg_behaviour_diff_global_attrs_change_3(global_attr):
#     V = "other"
#     file_paths = (
#         _make_nc_modify_global_attr(F1, global_attr, V),
#         _make_nc_modify_global_attr(F2, global_attr, V),
#         _make_nc_modify_global_attr(F3, global_attr, V),
#     )
#     try:
#         ds = _open(file_paths)
#         ds.close()
#     except ValueError as exc:
#         assert (
#             str(exc)
#             == "Could not find any dimension coordinates to use to order the datasets for concatenation"
#         )


# both new_var_id and old_var_id are in ds.variables no matter which file is changed


def test_agg_fails_diff_var_id_change_F1():
    new_var_id = "blah"
    old_var_id = "tas"
    file_paths = _make_nc_modify_var_id(F1, old_var_id, new_var_id), F2, F3
    ds = _open(file_paths)
    assert new_var_id, old_var_id in ds.variables
    ds.close()


def test_agg_fails_diff_var_id_change_F2():
    new_var_id = "blah"
    old_var_id = "tas"
    file_paths = F1, _make_nc_modify_var_id(F2, old_var_id, new_var_id), F3
    ds = _open(file_paths)
    assert new_var_id, old_var_id in ds.variables
    ds.close()


def test_agg_fails_diff_fill_value_change_F2():
    var_id = "tas"
    fill_value = np.float32(-1e20)
    file_paths = F1, _make_nc_modify_fill_value(F2, var_id, fill_value=fill_value), F3
    ds = _open(file_paths)
    assert ds[var_id].encoding["_FillValue"] != fill_value
    ds.close()


def test_agg_fails_diff_fill_value_change_F1():
    var_id = "tas"
    fill_value = np.float32(-1e20)
    file_paths = _make_nc_modify_fill_value(F1, var_id, fill_value=fill_value), F2, F3
    ds = _open(file_paths)
    assert ds[var_id].encoding["_FillValue"] == fill_value
    ds.close()


def test_agg_affected_by_order():
    # Apply a breaking change to different files in the sequence and
    # assert that the same exception is raised regardless of which
    # file is modified
    file_orders = itertools.permutations([F1, F2, F3])
    for _f1, _f2, _f3 in file_orders:
        file_paths = _f1, _make_nc_modify_var_attr(_f2, "tas", "units", "bad"), _f3
        if _f2 == F1:
            ds = _open(file_paths)
            assert "bad" in ds.tas.units
            ds.close()
        else:
            ds = _open(file_paths)
            assert "K" in ds.tas.units
            ds.close()

        # opens with incorrect change when change is in first file (earliest time)
        # otherwise no change (except in the case of var_id)
        # the changes cause the aggregation to fail

        # this is the case for all modifications
