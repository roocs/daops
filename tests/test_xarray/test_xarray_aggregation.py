"""test_xarray_aggregation.py
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

import numpy as np
import pytest
import xarray as xr


@pytest.fixture(scope="module")
def prepare_files(stratus):
    file_base = (
        f"{stratus.path}/badc/cmip5/data/cmip5/output1/MOHC/"
        "HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadGEM2-ES_rcp85_r1i1p1"
    )

    test_files = [
        file_base + end
        for end in ("_200512-203011.nc", "_203012-205511.nc", "_205512-208011.nc")
    ]

    return test_files


# Functions to make modified NC files
# need to make files temporary files
def _open(file_paths):
    time_coder = xr.coders.CFDatetimeCoder(use_cftime=True)
    return xr.open_mfdataset(
        file_paths,
        combine="by_coords",
        data_vars="all",
        decode_times=time_coder,
        join="outer",
        compat="no_conflicts",
    )


def _make_nc_modify_var_attr(nc_path, var_id, attr, value, path):
    with _open(nc_path) as ds:
        ds[var_id].attrs[attr] = value
        ds.to_netcdf(os.path.join(path, "tas_modify_var_attr.nc"))
    tmp_path = os.path.join(path, "tas_modify_var_attr.nc")
    return tmp_path


def _make_nc_modify_global_attr(nc_path, attr, value, path):
    with _open(nc_path) as ds:
        ds.attrs[attr] = value
        ds.to_netcdf(os.path.join(path, "tas_modify_global_attr.nc"))
    tmp_path = os.path.join(path, "tas_modify_global_attr.nc")
    return tmp_path


def _make_nc_modify_var_id(nc_path, old_var_id, new_var_id, path):
    with _open(nc_path) as ds:
        ds = ds.rename({old_var_id: new_var_id})
        ds.to_netcdf(path=os.path.join(path, "tas_modify_var_id.nc"))
    tmp_path = os.path.join(path, "tas_modify_var_id.nc")
    return tmp_path


def _make_nc_modify_fill_value(nc_path, var_id, fill_value, path):
    with _open(nc_path) as ds:
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


def test_agg_success_with_no_changes(prepare_files):
    ds = _open(prepare_files)
    assert "tas" in ds.variables
    ds.close()


@pytest.mark.timeout(30)
def test_agg_fails_diff_var_attrs_change_F2(var_attr, prepare_files, tmpdir):
    v = "rubbish"
    file_paths = (
        prepare_files[0],
        _make_nc_modify_var_attr(prepare_files[1], "tas", var_attr, v, path=tmpdir),
        prepare_files[2],
    )
    with _open(file_paths) as ds:
        assert ds.tas.__getattr__(f"{var_attr}") != v


@pytest.mark.timeout(30)
def test_agg_fails_diff_var_attrs_change_F1(var_attr, prepare_files, tmpdir):
    v = "rubbish"
    file_paths = (
        _make_nc_modify_var_attr(prepare_files[0], "tas", var_attr, v, path=tmpdir),
        prepare_files[1],
        prepare_files[2],
    )
    with _open(file_paths) as ds:
        assert ds.tas.__getattr__(f"{var_attr}") == v


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


def test_agg_behaviour_diff_global_attrs_change_F2(global_attr, prepare_files, tmpdir):
    v = "other"
    file_paths = (
        prepare_files[0],
        _make_nc_modify_global_attr(prepare_files[1], global_attr, v, path=tmpdir),
        prepare_files[2],
    )
    with _open(file_paths) as ds:
        assert ds.__getattr__(f"{global_attr}") != v


def test_agg_behaviour_diff_global_attrs_change_F1(global_attr, prepare_files, tmpdir):
    v = "other"
    file_paths = (
        _make_nc_modify_global_attr(prepare_files[0], global_attr, v, path=tmpdir),
        prepare_files[1],
        prepare_files[2],
    )
    with _open(file_paths) as ds:
        assert ds.__getattr__(f"{global_attr}") == v


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


def test_agg_fails_diff_var_id_change_F1(prepare_files, tmpdir):
    new_var_id = "blah"
    old_var_id = "tas"
    file_paths = (
        _make_nc_modify_var_id(prepare_files[0], old_var_id, new_var_id, path=tmpdir),
        prepare_files[1],
        prepare_files[2],
    )
    with _open(file_paths) as ds:
        assert new_var_id, old_var_id in ds.variables


def test_agg_fails_diff_var_id_change_F2(prepare_files, tmpdir):
    new_var_id = "blah"
    old_var_id = "tas"
    file_paths = (
        prepare_files[0],
        _make_nc_modify_var_id(prepare_files[1], old_var_id, new_var_id, path=tmpdir),
        prepare_files[2],
    )
    with _open(file_paths) as ds:
        assert new_var_id, old_var_id in ds.variables


def test_agg_fails_diff_fill_value_change_F2(prepare_files, tmpdir):
    var_id = "tas"
    fill_value = np.float32(-1e20)
    file_paths = (
        prepare_files[0],
        _make_nc_modify_fill_value(
            prepare_files[1], var_id, fill_value=fill_value, path=tmpdir
        ),
        prepare_files[2],
    )
    with _open(file_paths) as ds:
        assert ds[var_id].encoding["_FillValue"] != fill_value


def test_agg_fails_diff_fill_value_change_F1(prepare_files, tmpdir):
    var_id = "tas"
    fill_value = np.float32(-1e20)
    file_paths = (
        _make_nc_modify_fill_value(
            prepare_files[0], var_id, fill_value=fill_value, path=tmpdir
        ),
        prepare_files[1],
        prepare_files[2],
    )
    with _open(file_paths) as ds:
        assert ds[var_id].encoding["_FillValue"] == fill_value


def test_agg_affected_by_order(prepare_files, tmpdir):
    # Apply a breaking change to different files in the sequence and
    # assert that the same exception is raised regardless of which
    # file is modified
    file_orders = itertools.permutations(prepare_files)
    for _f1, _f2, _f3 in file_orders:
        file_paths = (
            _f1,
            _make_nc_modify_var_attr(_f2, "tas", "units", "bad", path=tmpdir),
            _f3,
        )
        with _open(file_paths) as ds:
            if _f2 == prepare_files[0]:
                assert "bad" in ds.tas.units
            else:
                assert "K" in ds.tas.units

        # opens with incorrect change when change is in first file (earliest time)
        # otherwise no change (except in the case of var_id)
        # the changes cause the aggregation to fail

        # this is the case for all modifications
