import re
from datetime import datetime

import cftime
import numpy as np

model_specific_global_attrs = {
    "CMCC-CM2-SR5": {
        "forcing_description": "f1, CMIP6 historical forcings",
        "physics_description": "physics from the standard model configuration, with no additional tuning or different parametrization",
        "initialization_description": "hindcast initialized based on observations and using historical forcing",
    },
    "EC-Earth3": {
        "forcing_description": "f1, CMIP6 historical forcings",
        "physics_description": "physics from the standard model configuration, with no additional tuning or different parametrization",
        "initialization_description": "Atmosphere initialization based on full-fields from ERA-Interim (s1979-s2018) or ERA-40 (s1960-s1978); ocean/sea-ice initialization based on full-fields from NEMO/LIM assimilation run nudged towards ORA-S4 (s1960-s2018)",
    },
    "HadGEM3-GC31-MM": {
        "forcing_description": "f2, CMIP6 v6.2.0 forcings; no ozone remapping",
        "physics_description": "physics from the standard model configuration, with no additional tuning or different parametrization",
        "initialization_description": "hindcast initialized based on observations and using historical forcing",
    },
    "MPI-ESM1-2-HR": {
        "forcing_description": "f1, CMIP6 historical forcings",
        "physics_description": "physics from the standard model configuration, with no additional tuning or different parametrization",
        "initialization_description": "hindcast initialized based on observations and using historical forcing",
    },
}


def get_time_calendar(ds_id, ds):
    times = ds.time.values
    cal = times[0].calendar
    return cal


def get_lead_times(ds_id, ds):
    start_date = datetime.fromisoformat(get_start_date(ds_id, ds))

    cal = get_time_calendar(ds_id, ds)
    reftime = cftime.datetime(
        start_date.year,
        start_date.month,
        start_date.day,
        start_date.hour,
        start_date.minute,
        start_date.second,
        calendar=cal,
    )

    lead_times = []
    # calculate leadtime from reftime and valid times
    for time in ds.time.values:
        td = time - reftime
        days = td.days
        lead_times.append(days)

    return lead_times


def get_start_date(ds_id, ds):
    year = ds_id.split(".")[5].split("-")[0].lstrip("s")
    sd = datetime(int(year), 11, 1, 0, 0).isoformat()
    return sd


def get_sub_experiment_id(ds_id, ds):
    sd = datetime.fromisoformat(get_start_date(ds_id, ds))
    se_id = f"s{sd.year}{sd.month}"
    return se_id


def get_reftime(ds_id, ds):
    default_sd = get_start_date(ds_id, ds)

    start_date = ds.attrs.get("startdate", None)

    if not start_date:
        start_date = default_sd

    else:
        #  attempt to get from startdate attribute - don't know if it will always be in sYYYYMM format?
        regex = re.compile(r"^s(\d{4})(\d{2})$")
        match = regex.match(start_date)

        default = datetime.fromisoformat(default_sd)

        if match:
            items = match.groups()
            try:
                start_date = datetime(
                    int(items[0]),
                    int(items[1]),
                    default.day,
                    default.hour,
                    default.minute,
                    default.second,
                ).isoformat()
            except ValueError:
                start_date = default_sd.isoformat()

        else:
            start_date = default_sd.isoformat()

    return start_date


def get_bnd_vars(ds_id, ds):
    bnd_vars = ["latitude", "longitude", "time"]
    bounds_list = [ds.cf.get_bounds(bv).name for bv in bnd_vars]
    return bounds_list


def get_decadal_bnds_list(ds_id, ds):
    bounds_list = get_bnd_vars(ds_id, ds)
    # coordinate attribute is always added to realization variable in decadal datasets
    bounds_list.append("realization")
    return bounds_list


def get_decadal_model_attr_from_dict(ds_id, ds, attr):
    # Add the model-specific global attr
    model = ds_id.split(".")[3]
    value = model_specific_global_attrs[model][attr]
    return value


def fix_further_info_url(ds_id, ds):
    model = ds_id.split(".")[3]
    further_info_url = ds.attrs.get("further_info_url", None)

    if "none" in further_info_url:
        year = get_sub_experiment_id(ds_id, ds)[:-2]
        return further_info_url.replace("none", year)

    else:
        return further_info_url
