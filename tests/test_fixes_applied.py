import math
import os

import cftime
import numpy as np
import pytest
import xarray as xr

from daops import CONFIG
from daops.ops.subset import subset
from tests._common import MINI_ESGF_MASTER_DIR


def _check_output_nc(result, fname="output_001.nc"):
    assert fname in [os.path.basename(_) for _ in result.file_uris]


@pytest.mark.online
def test_fixes_applied_decadal_MOHC_mon(tmpdir, load_esgf_test_data):
    # change fix index to test index which holds these decadal fixes
    fix_index = CONFIG["elasticsearch"]["fix_store"]
    test_fix_index = "c3s-roocs-fix"
    CONFIG["elasticsearch"]["fix_store"] = test_fix_index

    # don't use catalog - decadal datasets not in current catalog
    CONFIG["project:c3s-cmip6"]["use_catalog"] = False

    result = subset(
        "c3s-cmip6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004-r3i1p1f2.Amon.pr.gn.v20200417",
        output_dir=tmpdir,
        file_namer="simple",
    )

    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True, decode_timedelta=False)
    # check VarAttrFix is applied
    assert ds.time.long_name == "valid_time"

    # check GlobalAttrFix is applied
    assert ds.forcing_description == "f2, CMIP6 v6.2.0 forcings; no ozone remapping"
    assert (
        ds.initialization_description
        == "hindcast initialized based on observations and using historical forcing"
    )
    assert (
        ds.physics_description
        == "physics from the standard model configuration, with no additional tuning or different parametrization"
    )
    assert ds.startdate == "s200411"
    assert ds.sub_experiment_id == "s200411"

    # check further info url is unchanged
    assert (
        ds.further_info_url
        == "https://furtherinfo.es-doc.org/CMIP6.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s2004.r3i1p1f2"
    )

    # check AddScalarCoord Fix is applied
    assert "reftime" in ds.coords
    assert ds.reftime.dims == ()
    assert ds.reftime.encoding["calendar"] == ds.time.values[0].calendar
    assert ds.reftime.values == np.array(
        cftime.Datetime360Day(2004, 11, 1, 0, 0, 0, 0), dtype=object
    )

    # check AddCoordFix is applied
    assert "leadtime" in ds.coords
    assert ds.leadtime.dims == ("time",)
    assert ds.leadtime.values[0] == 15.0
    assert ds.leadtime.values[-1] == 3735.0
    assert ds.leadtime.units == "days"
    assert ds.leadtime.long_name == "Time elapsed since the start of the forecast"
    assert ds.leadtime.standard_name == "forecast_period"

    # check AddDataVarFix is applied
    assert "realization" in ds.data_vars
    assert ds.realization.values == np.array(1, dtype=np.int32)
    assert (
        ds.realization.comment
        == "For more information on the ripf, refer to the variant_label, initialization_description, physics_description and forcing_description global attributes"
    )

    # check coordinate attribute removed from realization and bounds variables
    assert ds.realization.encoding.get("coordinates") is None
    assert ds.lon_bnds.encoding.get("coordinates") is None
    assert ds.lat_bnds.encoding.get("coordinates") is None
    assert ds.time_bnds.encoding.get("coordinates") is None

    # change fix index back
    CONFIG["elasticsearch"]["fix_store"] = fix_index


@pytest.mark.online
def test_fixes_applied_decadal_MOHC_day(tmpdir, load_esgf_test_data):
    # change fix index to test index which holds these decadal fixes
    fix_index = CONFIG["elasticsearch"]["fix_store"]
    test_fix_index = "c3s-roocs-fix"
    CONFIG["elasticsearch"]["fix_store"] = test_fix_index

    # don't use catalog - decadal datasets not in current catalog
    CONFIG["project:c3s-cmip6"]["use_catalog"] = False

    result = subset(
        "c3s-cmip6.DCPP.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s1960-r2i1p1f2.day.tasmin.gn.v20200417",
        output_dir=tmpdir,
        file_namer="simple",
    )

    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True, decode_timedelta=False)

    # check VarAttrFix is applied
    assert ds.time.long_name == "valid_time"

    # check GlobalAttrFix is applied
    assert ds.forcing_description == "f2, CMIP6 v6.2.0 forcings; no ozone remapping"
    assert (
        ds.initialization_description
        == "hindcast initialized based on observations and using historical forcing"
    )
    assert (
        ds.physics_description
        == "physics from the standard model configuration, with no additional tuning or different parametrization"
    )
    assert ds.startdate == "s196011"
    assert ds.sub_experiment_id == "s196011"

    # check further info url is unchanged
    assert (
        ds.further_info_url
        == "https://furtherinfo.es-doc.org/CMIP6.MOHC.HadGEM3-GC31-MM.dcppA-hindcast.s1960.r2i1p1f2"
    )

    # check AddScalarCoord Fix is applied
    assert "reftime" in ds.coords
    assert ds.reftime.dims == ()
    assert ds.reftime.encoding["calendar"] == ds.time.values[0].calendar
    assert ds.reftime.values == np.array(
        cftime.Datetime360Day(1960, 11, 1, 0, 0, 0, 0), dtype=object
    )

    # check AddCoordFix is applied
    assert "leadtime" in ds.coords
    assert ds.leadtime.dims == ("time",)
    assert ds.leadtime.values[0] == 0.0
    assert ds.leadtime.values[-1] == 419.0
    assert ds.leadtime.units == "days"
    assert ds.leadtime.long_name == "Time elapsed since the start of the forecast"
    assert ds.leadtime.standard_name == "forecast_period"

    # check AddDataVarFix is applied
    assert "realization" in ds.data_vars
    assert ds.realization.values == np.array(1, dtype=np.int32)
    assert (
        ds.realization.comment
        == "For more information on the ripf, refer to the variant_label, initialization_description, physics_description and forcing_description global attributes"
    )

    # check coordinate attribute removed from realization and bounds variables
    assert ds.realization.encoding.get("coordinates") is None
    assert ds.lon_bnds.encoding.get("coordinates") is None
    assert ds.lat_bnds.encoding.get("coordinates") is None
    assert ds.time_bnds.encoding.get("coordinates") is None

    # change fix index back
    CONFIG["elasticsearch"]["fix_store"] = fix_index


@pytest.mark.online
def test_fixes_applied_decadal_EC_Earth_mon(tmpdir, load_esgf_test_data):
    # change fix index to test index which holds these decadal fixes
    fix_index = CONFIG["elasticsearch"]["fix_store"]
    test_fix_index = "c3s-roocs-fix"
    CONFIG["elasticsearch"]["fix_store"] = test_fix_index

    # don't use catalog - decadal datasets not in current catalog
    CONFIG["project:c3s-cmip6"]["use_catalog"] = False

    result = subset(
        "c3s-cmip6.DCPP.EC-Earth-Consortium.EC-Earth3.dcppA-hindcast.s1960-r6i2p1f1.Amon.tas.gr.v20200508",
        output_dir=tmpdir,
        file_namer="simple",
    )

    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True, decode_timedelta=False)
    # check VarAttrFix is applied
    assert ds.time.long_name == "valid_time"

    # check GlobalAttrFix is applied
    assert ds.forcing_description == "f1, CMIP6 historical forcings"
    assert (
        ds.initialization_description
        == "Atmosphere initialization based on full-fields from ERA-Interim (s1979-s2018) or ERA-40 (s1960-s1978); ocean/sea-ice initialization based on full-fields from NEMO/LIM assimilation run nudged towards ORA-S4 (s1960-s2018)"
    )
    assert (
        ds.physics_description
        == "physics from the standard model configuration, with no additional tuning or different parametrization"
    )
    assert ds.startdate == "s196011"
    assert ds.sub_experiment_id == "s196011"

    # check further info url is unchanged
    assert (
        ds.further_info_url
        == "https://furtherinfo.es-doc.org/CMIP6.EC-Earth-Consortium.EC-Earth3.dcppA-hindcast.s1960.r6i2p1f1"
    )

    # check AddScalarCoord Fix is applied
    assert "reftime" in ds.coords
    assert ds.reftime.dims == ()
    assert ds.reftime.encoding["calendar"] == ds.time.values[0].calendar
    assert ds.reftime.values == np.array(
        cftime.DatetimeProlepticGregorian(1960, 11, 1, 0, 0, 0, 0), dtype=object
    )

    # check AddCoordFix is applied
    assert "leadtime" in ds.coords
    assert ds.leadtime.dims == ("time",)
    assert ds.leadtime.values[0] == 15.0
    assert ds.leadtime.values[-1] == 410.0
    assert ds.leadtime.units == "days"
    assert ds.leadtime.long_name == "Time elapsed since the start of the forecast"
    assert ds.leadtime.standard_name == "forecast_period"

    # check AddDataVarFix is applied
    assert "realization" in ds.data_vars
    assert ds.realization.values == np.array(1, dtype=np.int32)
    assert (
        ds.realization.comment
        == "For more information on the ripf, refer to the variant_label, initialization_description, physics_description and forcing_description global attributes"
    )

    # check coordinate attribute removed from realization and bounds variables
    assert ds.realization.encoding.get("coordinates") is None
    assert ds.lon_bnds.encoding.get("coordinates") is None
    assert ds.lat_bnds.encoding.get("coordinates") is None
    assert ds.time_bnds.encoding.get("coordinates") is None

    # change fix index back
    CONFIG["elasticsearch"]["fix_store"] = fix_index


@pytest.mark.online
def test_fixes_applied_decadal_EC_Earth_day(tmpdir, load_esgf_test_data):
    # change fix index to test index which holds these decadal fixes
    fix_index = CONFIG["elasticsearch"]["fix_store"]
    test_fix_index = "c3s-roocs-fix"
    CONFIG["elasticsearch"]["fix_store"] = test_fix_index

    # don't use catalog - decadal datasets not in current catalog
    CONFIG["project:c3s-cmip6"]["use_catalog"] = False

    result = subset(
        "c3s-cmip6.DCPP.EC-Earth-Consortium.EC-Earth3.dcppA-hindcast.s1961-r6i2p1f1.day.pr.gr.v20200508",
        output_dir=tmpdir,
        file_namer="simple",
    )

    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True, decode_timedelta=False)
    # check VarAttrFix is applied
    assert ds.time.long_name == "valid_time"

    # check GlobalAttrFix is applied
    assert ds.forcing_description == "f1, CMIP6 historical forcings"
    assert (
        ds.initialization_description
        == "Atmosphere initialization based on full-fields from ERA-Interim (s1979-s2018) or ERA-40 (s1960-s1978); ocean/sea-ice initialization based on full-fields from NEMO/LIM assimilation run nudged towards ORA-S4 (s1960-s2018)"
    )
    assert (
        ds.physics_description
        == "physics from the standard model configuration, with no additional tuning or different parametrization"
    )
    assert ds.startdate == "s196111"
    assert ds.sub_experiment_id == "s196111"

    # check further info url is unchanged
    assert (
        ds.further_info_url
        == "https://furtherinfo.es-doc.org/CMIP6.EC-Earth-Consortium.EC-Earth3.dcppA-hindcast.s1961.r6i2p1f1"
    )

    # check AddScalarCoord Fix is applied
    assert "reftime" in ds.coords
    assert ds.reftime.dims == ()
    assert ds.reftime.encoding["calendar"] == ds.time.values[0].calendar
    assert ds.reftime.values == np.array(
        cftime.DatetimeProlepticGregorian(1961, 11, 1, 0, 0, 0, 0), dtype=object
    )

    # check AddCoordFix is applied
    assert "leadtime" in ds.coords
    assert ds.leadtime.dims == ("time",)
    assert ds.leadtime.values[0] == 0.0
    assert ds.leadtime.values[-1] == 425.0
    assert ds.leadtime.units == "days"
    assert ds.leadtime.long_name == "Time elapsed since the start of the forecast"
    assert ds.leadtime.standard_name == "forecast_period"

    # check AddDataVarFix is applied
    assert "realization" in ds.data_vars
    assert ds.realization.values == np.array(1, dtype=np.int32)
    assert (
        ds.realization.comment
        == "For more information on the ripf, refer to the variant_label, initialization_description, physics_description and forcing_description global attributes"
    )

    # check coordinate attribute removed from realization and bounds variables
    assert ds.realization.encoding.get("coordinates") is None
    assert ds.lon_bnds.encoding.get("coordinates") is None
    assert ds.lat_bnds.encoding.get("coordinates") is None
    assert ds.time_bnds.encoding.get("coordinates") is None

    # change fix index back
    CONFIG["elasticsearch"]["fix_store"] = fix_index


@pytest.mark.online
def test_fixes_applied_decadal_EC_Earth_url_fix(tmpdir, load_esgf_test_data):
    # change fix index to test index which holds these decadal fixes
    fix_index = CONFIG["elasticsearch"]["fix_store"]
    test_fix_index = "c3s-roocs-fix"
    CONFIG["elasticsearch"]["fix_store"] = test_fix_index

    # don't use catalog - decadal datasets not in current catalog
    CONFIG["project:c3s-cmip6"]["use_catalog"] = False

    result = subset(
        "c3s-cmip6.DCPP.EC-Earth-Consortium.EC-Earth3.dcppA-hindcast.s1960-r2i1p1f1.Amon.tas.gr.v20201215",
        output_dir=tmpdir,
        file_namer="simple",
    )

    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True, decode_timedelta=False)
    # check VarAttrFix is applied
    assert ds.time.long_name == "valid_time"

    # check GlobalAttrFix is applied
    assert ds.forcing_description == "f1, CMIP6 historical forcings"
    assert (
        ds.initialization_description
        == "Atmosphere initialization based on full-fields from ERA-Interim (s1979-s2018) or ERA-40 (s1960-s1978); ocean/sea-ice initialization based on full-fields from NEMO/LIM assimilation run nudged towards ORA-S4 (s1960-s2018)"
    )
    assert (
        ds.physics_description
        == "physics from the standard model configuration, with no additional tuning or different parametrization"
    )
    assert ds.startdate == "s196011"
    assert ds.sub_experiment_id == "s196011"

    # check further info url is unchanged
    assert (
        ds.further_info_url
        == "https://furtherinfo.es-doc.org/CMIP6.EC-Earth-Consortium.EC-Earth3.dcppA-hindcast.s1960.r2i1p1f1"
    )

    # check AddScalarCoord Fix is applied
    assert "reftime" in ds.coords
    assert ds.reftime.dims == ()
    assert ds.reftime.encoding["calendar"] == ds.time.values[0].calendar
    assert ds.reftime.values == np.array(
        cftime.DatetimeGregorian(1960, 11, 1, 0, 0, 0, 0), dtype=object
    )

    # check AddCoordFix is applied
    assert "leadtime" in ds.coords
    assert ds.leadtime.dims == ("time",)
    assert ds.leadtime.values[0] == 15.0
    assert ds.leadtime.values[-1] == 714.0
    assert ds.leadtime.units == "days"
    assert ds.leadtime.long_name == "Time elapsed since the start of the forecast"
    assert ds.leadtime.standard_name == "forecast_period"

    # check AddDataVarFix is applied
    assert "realization" in ds.data_vars
    assert ds.realization.values == np.array(1, dtype=np.int32)
    assert (
        ds.realization.comment
        == "For more information on the ripf, refer to the variant_label, initialization_description, physics_description and forcing_description global attributes"
    )

    # check coordinate attribute removed from realization and bounds variables
    assert ds.realization.encoding.get("coordinates") is None
    assert ds.lon_bnds.encoding.get("coordinates") is None
    assert ds.lat_bnds.encoding.get("coordinates") is None
    assert ds.time_bnds.encoding.get("coordinates") is None

    # change fix index back
    CONFIG["elasticsearch"]["fix_store"] = fix_index


@pytest.mark.online
def test_fixes_applied_decadal_MPI_M_mon(tmpdir, load_esgf_test_data):
    # change fix index to test index which holds these decadal fixes
    fix_index = CONFIG["elasticsearch"]["fix_store"]
    test_fix_index = "c3s-roocs-fix"
    CONFIG["elasticsearch"]["fix_store"] = test_fix_index

    # don't use catalog - decadal datasets not in current catalog
    CONFIG["project:c3s-cmip6"]["use_catalog"] = False

    result = subset(
        "c3s-cmip6.DCPP.MPI-M.MPI-ESM1-2-HR.dcppA-hindcast.s1960-r10i1p1f1.Amon.tas.gn.v20200908",
        output_dir=tmpdir,
        file_namer="simple",
    )

    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True, decode_timedelta=False)

    # check VarAttrFix is applied
    assert ds.time.long_name == "valid_time"

    # check GlobalAttrFix is applied
    assert ds.forcing_description == "f1, CMIP6 historical forcings"
    assert (
        ds.initialization_description
        == "hindcast initialized based on observations and using historical forcing"
    )
    assert (
        ds.physics_description
        == "physics from the standard model configuration, with no additional tuning or different parametrization"
    )
    assert ds.startdate == "s196011"
    assert ds.sub_experiment_id == "s196011"

    # check further info url is unchanged
    assert (
        ds.further_info_url
        == "https://furtherinfo.es-doc.org/CMIP6.MPI-M.MPI-ESM1-2-HR.dcppA-hindcast.s1960.r10i1p1f1"
    )

    # check AddScalarCoord Fix is applied
    assert "reftime" in ds.coords
    assert ds.reftime.dims == ()
    assert ds.reftime.encoding["calendar"] == ds.time.values[0].calendar
    assert ds.reftime.values == np.array(
        cftime.DatetimeGregorian(1960, 11, 1, 0, 0, 0, 0), dtype=object
    )

    # check AddCoordFix is applied
    assert "leadtime" in ds.coords
    assert ds.leadtime.dims == ("time",)
    assert ds.leadtime.values[0] == 15.0
    assert ds.leadtime.values[-1] == 3697.0
    assert ds.leadtime.units == "days"
    assert ds.leadtime.long_name == "Time elapsed since the start of the forecast"
    assert ds.leadtime.standard_name == "forecast_period"

    # check AddDataVarFix is applied
    assert "realization" in ds.data_vars
    assert ds.realization.values == np.array(1, dtype=np.int32)
    assert (
        ds.realization.comment
        == "For more information on the ripf, refer to the variant_label, initialization_description, physics_description and forcing_description global attributes"
    )

    # check coordinate attribute removed from realization and bounds variables
    assert ds.realization.encoding.get("coordinates") is None
    assert ds.lon_bnds.encoding.get("coordinates") is None
    assert ds.lat_bnds.encoding.get("coordinates") is None
    assert ds.time_bnds.encoding.get("coordinates") is None

    # change fix index back
    CONFIG["elasticsearch"]["fix_store"] = fix_index


@pytest.mark.online
def test_fixes_applied_decadal_MPI_M_day(tmpdir, load_esgf_test_data):
    # change fix index to test index which holds these decadal fixes
    fix_index = CONFIG["elasticsearch"]["fix_store"]
    test_fix_index = "c3s-roocs-fix"
    CONFIG["elasticsearch"]["fix_store"] = test_fix_index

    # don't use catalog - decadal datasets not in current catalog
    CONFIG["project:c3s-cmip6"]["use_catalog"] = False

    result = subset(
        "c3s-cmip6.DCPP.MPI-M.MPI-ESM1-2-HR.dcppA-hindcast.s1960-r2i1p1f1.day.pr.gn.v20190929",
        output_dir=tmpdir,
        file_namer="simple",
    )

    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True, decode_timedelta=False)

    # check VarAttrFix is applied
    assert ds.time.long_name == "valid_time"

    # check GlobalAttrFix is applied
    assert ds.forcing_description == "f1, CMIP6 historical forcings"
    assert (
        ds.initialization_description
        == "hindcast initialized based on observations and using historical forcing"
    )
    assert (
        ds.physics_description
        == "physics from the standard model configuration, with no additional tuning or different parametrization"
    )
    assert ds.startdate == "s196011"
    assert ds.sub_experiment_id == "s196011"

    # check further info url is unchanged
    assert (
        ds.further_info_url
        == "https://furtherinfo.es-doc.org/CMIP6.MPI-M.MPI-ESM1-2-HR.dcppA-hindcast.s1960.r2i1p1f1"
    )

    # check AddScalarCoord Fix is applied
    assert "reftime" in ds.coords
    assert ds.reftime.dims == ()
    assert ds.reftime.encoding["calendar"] == ds.time.values[0].calendar
    assert ds.reftime.values == np.array(
        cftime.DatetimeGregorian(1960, 11, 1, 0, 0, 0, 0), dtype=object
    )

    # check AddCoordFix is applied
    assert "leadtime" in ds.coords
    assert ds.leadtime.dims == ("time",)
    assert ds.leadtime.values[0] == 0.0
    assert ds.leadtime.values[-1] == 3712.0
    assert ds.leadtime.units == "days"
    assert ds.leadtime.long_name == "Time elapsed since the start of the forecast"
    assert ds.leadtime.standard_name == "forecast_period"

    # check AddDataVarFix is applied
    assert "realization" in ds.data_vars
    assert ds.realization.values == np.array(1, dtype=np.int32)
    assert (
        ds.realization.comment
        == "For more information on the ripf, refer to the variant_label, initialization_description, physics_description and forcing_description global attributes"
    )

    # check coordinate attribute removed from realization and bounds variables
    assert ds.realization.encoding.get("coordinates") is None
    assert ds.lon_bnds.encoding.get("coordinates") is None
    assert ds.lat_bnds.encoding.get("coordinates") is None
    assert ds.time_bnds.encoding.get("coordinates") is None

    # change fix index back
    CONFIG["elasticsearch"]["fix_store"] = fix_index


@pytest.mark.online
def test_fixes_applied_decadal_CMCC_mon(tmpdir, load_esgf_test_data):
    # change fix index to test index which holds these decadal fixes
    fix_index = CONFIG["elasticsearch"]["fix_store"]
    test_fix_index = "c3s-roocs-fix"
    CONFIG["elasticsearch"]["fix_store"] = test_fix_index

    # don't use catalog - decadal datasets not in current catalog
    CONFIG["project:c3s-cmip6"]["use_catalog"] = False

    result = subset(
        "c3s-cmip6.DCPP.CMCC.CMCC-CM2-SR5.dcppA-hindcast.s1960-r10i1p1f1.Amon.pr.gn.v20210719",
        output_dir=tmpdir,
        file_namer="simple",
    )

    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True, decode_timedelta=False)

    # check VarAttrFix is applied
    assert ds.time.long_name == "valid_time"

    # check GlobalAttrFix is applied
    assert ds.forcing_description == "f1, CMIP6 historical forcings"
    assert (
        ds.initialization_description
        == "hindcast initialized based on observations and using historical forcing"
    )
    assert (
        ds.physics_description
        == "physics from the standard model configuration, with no additional tuning or different parametrization"
    )
    assert ds.startdate == "s196011"
    assert ds.sub_experiment_id == "s196011"

    # check further info url is unchanged
    assert (
        ds.further_info_url
        == "https://furtherinfo.es-doc.org/CMIP6.CMCC.CMCC-CM2-SR5.dcppA-hindcast.s1960.r10i1p1f1"
    )

    # check AddScalarCoord Fix is applied
    assert "reftime" in ds.coords
    assert ds.reftime.dims == ()
    assert ds.reftime.encoding["calendar"] == ds.time.values[0].calendar
    assert ds.reftime.values == np.array(
        cftime.DatetimeNoLeap(1960, 11, 1, 0, 0, 0, 0), dtype=object
    )

    # check AddCoordFix is applied
    assert "leadtime" in ds.coords
    assert ds.leadtime.dims == ("time",)
    assert ds.leadtime.values[0] == 15.0
    assert ds.leadtime.values[-1] == 3695.0
    assert ds.leadtime.units == "days"
    assert ds.leadtime.long_name == "Time elapsed since the start of the forecast"
    assert ds.leadtime.standard_name == "forecast_period"

    # check AddDataVarFix is applied
    assert "realization" in ds.data_vars
    assert ds.realization.values == np.array(1, dtype=np.int32)
    assert (
        ds.realization.comment
        == "For more information on the ripf, refer to the variant_label, initialization_description, physics_description and forcing_description global attributes"
    )

    # check coordinate attribute removed from realization and bounds variables
    assert ds.realization.encoding.get("coordinates") is None
    assert ds.lon_bnds.encoding.get("coordinates") is None
    assert ds.lat_bnds.encoding.get("coordinates") is None
    assert ds.time_bnds.encoding.get("coordinates") is None

    # change fix index back
    CONFIG["elasticsearch"]["fix_store"] = fix_index


@pytest.mark.skip(reason="no CMCC day datasets on c3s fix index")
@pytest.mark.online
def test_fixes_applied_decadal_CMCC_day(tmpdir, load_esgf_test_data):
    # change fix index to test index which holds these decadal fixes
    fix_index = CONFIG["elasticsearch"]["fix_store"]
    test_fix_index = "c3s-roocs-fix"
    CONFIG["elasticsearch"]["fix_store"] = test_fix_index

    # don't use catalog - decadal datasets not in current catalog
    CONFIG["project:c3s-cmip6"]["use_catalog"] = False

    result = subset(
        "c3s-cmip6.DCPP.CMCC.CMCC-CM2-SR5.dcppA-hindcast.s1960-r1i1p1f1.day.tas.gn.v20210806",
        output_dir=tmpdir,
        file_namer="simple",
    )

    _check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True, decode_timedelta=False)

    # check VarAttrFix is applied
    assert ds.time.long_name == "valid_time"

    # check GlobalAttrFix is applied
    assert ds.forcing_description == "f1, CMIP6 historical forcings"
    assert (
        ds.initialization_description
        == "hindcast initialized based on observations and using historical forcing"
    )
    assert (
        ds.physics_description
        == "physics from the standard model configuration, with no additional tuning or different parametrization"
    )
    assert ds.startdate == "s196011"
    assert ds.sub_experiment_id == "s196011"

    # check further info url is unchanged
    assert (
        ds.further_info_url
        == "https://furtherinfo.es-doc.org/CMIP6.CMCC.CMCC-CM2-SR5.dcppA-hindcast.s1960.r1i1p1f1"
    )

    # check AddScalarCoord Fix is applied
    assert "reftime" in ds.coords
    assert ds.reftime.dims == ()
    assert ds.reftime.encoding["calendar"] == ds.time.values[0].calendar
    assert ds.reftime.values == np.array(
        cftime.DatetimeGregorian(1960, 11, 1, 0, 0, 0, 0), dtype=object
    )

    # check AddCoordFix is applied
    assert "leadtime" in ds.coords
    assert ds.leadtime.dims == ("time",)
    assert ds.leadtime.values[0] == 0.0
    assert ds.leadtime.values[-1] == 3710.0
    assert ds.leadtime.units == "days"
    assert ds.leadtime.long_name == "Time elapsed since the start of the forecast"
    assert ds.leadtime.standard_name == "forecast_period"

    # check AddDataVarFix is applied
    assert "realization" in ds.data_vars
    assert ds.realization.values == np.array(1, dtype=np.int32)
    assert (
        ds.realization.comment
        == "For more information on the ripf, refer to the variant_label, initialization_description, physics_description and forcing_description global attributes"
    )

    # check coordinate attribute removed from realization and bounds variables
    assert ds.realization.encoding.get("coordinates") is None
    assert ds.lon_bnds.encoding.get("coordinates") is None
    assert ds.lat_bnds.encoding.get("coordinates") is None
    assert ds.time_bnds.encoding.get("coordinates") is None

    # change fix index back
    CONFIG["elasticsearch"]["fix_store"] = fix_index
