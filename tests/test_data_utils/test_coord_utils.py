import numpy as np
import xarray as xr
from daops.data_utils.coord_utils import add_coord, add_scalar_coord, squeeze_dims
from clisops.utils.dataset_utils import open_xr_dataset
from xarray.coders import CFDatetimeCoder

TIME_CODER = CFDatetimeCoder(use_cftime=True)


def test_squeeze_dims(stratus):
    ds = xr.open_mfdataset(
        f"{stratus.path}/badc/cmip5/data/cmip5/output1/INM/"
        "inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc",
        combine="by_coords",
        decode_times=TIME_CODER,
    )
    ds_id = "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"

    assert "lev" in ds.dims

    operands = {"dims": ["lev"]}

    ds_squeeze = squeeze_dims(ds_id, ds, **operands)
    assert "lev" not in ds_squeeze.dims


def test_add_scalar_coord(stratus):
    ds_no_height = xr.open_mfdataset(
        f"{stratus.path}/badc/cmip5/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        combine="by_coords",
        decode_times=TIME_CODER,
        data_vars="all",
    )
    ds_id = "cmip5.output1.ICHEC.EC-EARTH.historical.mon.atmos.Amon.r1i1p1.latest.tas"

    ds_with_height = xr.open_mfdataset(
        f"{stratus.path}/badc/cmip5/data/cmip5/output1/INM/inmcm4/historical/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
        combine="by_coords",
        decode_times=TIME_CODER,
    )
    operands = {
        "dtype": "float64",
        "value": "2.0",
        "var_id": "height",
        "attrs": {
            "axis": "Z",
            "long_name": "height",
            "positive": "up",
            "standard_name": "height",
            "units": "m",
        },
    }
    ds_no_height = add_scalar_coord(ds_id, ds_no_height, **operands)
    assert ds_no_height.height == ds_with_height.height
    assert ds_no_height.height.attrs == ds_with_height.height.attrs


def test_add_scalar_coord_with_derive(mini_esgf_data):
    ds_no_reftime = open_xr_dataset(mini_esgf_data["CMIP6_DECADAL"])
    ds_id = "CMIP6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417"

    operands = {
        "var_id": "reftime",
        "value": "derive: daops.fix_utils.decadal_utils.get_reftime",
        "dtype": "datetime64[ns]",
        "attrs": {
            "long_name": "Start date of the forecast",
            "standard_name": "forecast_reference_time",
        },
        "encoding": {
            "dtype": "int32",
            "units": "days since 1850-01-01",
            "calendar": "gregorian",
        },
    }
    ds_reftime = add_scalar_coord(ds_id, ds_no_reftime, **operands)
    assert "reftime" in ds_reftime.coords
    assert ds_reftime.reftime.dims == ()
    value = np.datetime_as_string(ds_reftime.reftime.values, unit="s")
    assert value == "2004-11-01T00:00:00"


def test_add_coord(stratus):
    ds_no_leadtime = xr.open_mfdataset(
        f"{stratus.path}/badc/cmip5/data/cmip5/output1/ICHEC/EC-EARTH/historical/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_EC-EARTH_historical_r1i1p1_185001-185912.nc",
        combine="by_coords",
        decode_times=TIME_CODER,
    )
    ds_id = "cmip5.output1.ICHEC.EC-EARTH.historical.mon.atmos.Amon.r1i1p1.latest.tas"

    operands = {
        "var_id": "leadtime",
        "value": np.zeros(120),
        "dim": ["time"],
        "dtype": "timedelta64[D]",
        "attrs": {
            "long_name": "Time elapsed since the start of the forecast",
            "standard_name": "forecast_period",
        },
        "encoding": {"dtype": "double"},
    }

    ds_with_leadtime = add_coord(ds_id, ds_no_leadtime, **operands)

    assert "leadtime" in ds_with_leadtime.coords
    assert (
        ds_with_leadtime.leadtime.attrs["long_name"]
        == "Time elapsed since the start of the forecast"
    )


def test_add_coord_with_derive(mini_esgf_data):
    ds_no_leadtime = open_xr_dataset(mini_esgf_data["CMIP6_DECADAL"])
    ds_id = "CMIP6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417"

    operands = {
        "var_id": "leadtime",
        "value": "derive: daops.fix_utils.decadal_utils.get_lead_times",
        "dim": ["time"],
        "dtype": "timedelta64[D]",
        "attrs": {
            "long_name": "Time elapsed since the start of the forecast",
            "standard_name": "forecast_period",
        },
        "encoding": {"dtype": "double"},
    }

    ds_leadtime = add_coord(ds_id, ds_no_leadtime, **operands)

    assert "leadtime" in ds_leadtime.coords
    assert ds_leadtime.leadtime.dims == ("time",)
    assert ds_leadtime.leadtime.values[0].astype("timedelta64[D]").astype(int) == 15.0
    assert ds_leadtime.leadtime.values[-1].astype("timedelta64[D]").astype(int) == 45.0
    assert (
        ds_leadtime.leadtime.long_name == "Time elapsed since the start of the forecast"
    )
    assert ds_leadtime.leadtime.standard_name == "forecast_period"
