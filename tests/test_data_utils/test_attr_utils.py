import xarray as xr
from daops.data_utils.attr_utils import (
    add_global_attrs_if_needed,
    edit_global_attrs,
    edit_var_attrs,
)
from clisops.utils.dataset_utils import open_xr_dataset
from xarray.coders import CFDatetimeCoder

TIME_CODER = CFDatetimeCoder(use_cftime=True)


def test_edit_var_attrs(stratus):
    ds = xr.open_mfdataset(
        f"{stratus.path}/badc/cmip5/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_EC-EARTH_historical_r1i1p1_185001-185912.nc",
        combine="by_coords",
        decode_times=TIME_CODER,
    )

    ds_id = "cmip5.output1.ICHEC.EC-EARTH.historical.mon.atmos.Amon.r1i1p1.latest.tas"

    assert ds.lat.attrs["standard_name"] == "latitude"
    assert ds.lat.attrs["long_name"] == "latitude"

    operands = {
        "var_id": "lat",
        "attrs": {
            "long_name": "False long name",
            "standard_name": "fake_standard_name",
        },
    }
    ds_change_var_attrs = edit_var_attrs(ds_id, ds, **operands)
    assert ds_change_var_attrs.lat.attrs["standard_name"] == "fake_standard_name"
    assert ds_change_var_attrs.lat.attrs["long_name"] == "False long name"


def test_edit_global_attrs(stratus):
    ds = xr.open_mfdataset(
        f"{stratus.path}/badc/cmip5/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_EC-EARTH_historical_r1i1p1_185001-185912.nc",
        combine="by_coords",
        decode_times=TIME_CODER,
    )
    ds_id = "cmip5.output1.ICHEC.EC-EARTH.historical.mon.atmos.Amon.r1i1p1.latest.tas"

    assert (
        ds.attrs["comment"]
        == "Equilibrium reached after preindustrial spin-up after which data were output starting with nominal date of January 1850"
    )
    assert ds.attrs["title"] == "EC-EARTH model output prepared for CMIP5 historical"
    assert ds.attrs.get("test", None) is None

    operands = {
        "attrs": {
            "comment": "this is a test commment",
            "title": "this is a test title",
            "test": "this is a new test attribute",
        }
    }
    ds_change_global_attrs = edit_global_attrs(ds_id, ds, **operands)

    assert ds_change_global_attrs.attrs["comment"] == "this is a test commment"
    assert ds_change_global_attrs.attrs["title"] == "this is a test title"
    assert ds_change_global_attrs.attrs["test"] == "this is a new test attribute"


def test_edit_global_attrs_with_derive(mini_esgf_data):
    ds = open_xr_dataset(mini_esgf_data["CMIP6_DECADAL"])
    ds_id = "CMIP6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417"

    assert ds.attrs.get("startdate") is None
    assert ds.attrs.get("sub_experiment_id")

    operands = {
        "attrs": {
            "startdate": "derive: daops.fix_utils.decadal_utils.get_sub_experiment_id",
            "sub_experiment_id": "derive: daops.fix_utils.decadal_utils.get_sub_experiment_id",
        }
    }
    ds_change_global_attrs = edit_global_attrs(ds_id, ds, **operands)

    assert ds_change_global_attrs.attrs["startdate"] == "s200411"
    assert ds_change_global_attrs.attrs["sub_experiment_id"] == "s200411"


def test_edit_global_attrs_with_derive_and_arg(mini_esgf_data):
    ds = open_xr_dataset(mini_esgf_data["CMIP6_DECADAL"])
    ds_id = "CMIP6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417"

    assert ds.attrs.get("forcing_description") is None

    operands = {
        "attrs": {
            "forcing_description": "derive: daops.fix_utils.decadal_utils.get_decadal_model_attr_from_dict: forcing_description",
        }
    }
    ds_change_global_attrs = edit_global_attrs(ds_id, ds, **operands)

    assert (
        ds_change_global_attrs.attrs["forcing_description"]
        == "f2, CMIP6 v6.2.0 forcings; no ozone remapping"
    )


def test_add_global_attrs_if_needed(stratus):
    ds = xr.open_mfdataset(
        f"{stratus.path}/badc/cmip5/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_EC-EARTH_historical_r1i1p1_185001-185912.nc",
        combine="by_coords",
        decode_times=TIME_CODER,
    )

    ds_id = "cmip5.output1.ICHEC.EC-EARTH.historical.mon.atmos.Amon.r1i1p1.latest.tas"

    assert (
        ds.attrs["comment"]
        == "Equilibrium reached after preindustrial spin-up after which data were output starting with nominal date of January 1850"
    )
    assert ds.attrs["title"] == "EC-EARTH model output prepared for CMIP5 historical"
    assert ds.attrs.get("test", None) is None

    operands = {
        "attrs": {
            "comment": "this is a test commment",
            "title": "this is a test title",
            "test": "this is a new test attribute",
        }
    }
    ds_change_global_attrs = add_global_attrs_if_needed(ds_id, ds, **operands)

    assert (
        ds_change_global_attrs.attrs["comment"]
        == "Equilibrium reached after preindustrial spin-up after which data were output starting with nominal date of January 1850"
    )
    assert (
        ds_change_global_attrs.attrs["title"]
        == "EC-EARTH model output prepared for CMIP5 historical"
    )
    assert ds_change_global_attrs.attrs["test"] == "this is a new test attribute"
