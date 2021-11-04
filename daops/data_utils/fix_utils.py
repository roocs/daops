from datetime import datetime
from pydoc import locate

import numpy as np


def handle_derive_str(value, ds_id, ds):
    if isinstance(value, str) and "derive" in value:
        func = locate(value.split(":")[1].strip())
        return func(ds_id, ds)
    else:
        return value


def get_lead_times(ds_id, ds):

    start_date = datetime.fromisoformat(get_start_date(ds_id, ds))

    times = ds.time.values.astype("datetime64[ns]")
    reftime = np.datetime64(start_date)
    lead_times = []

    # calculate leadtime from reftime and valid times
    for time in times:
        td = time - reftime
        days = td.astype("timedelta64[D]")
        days = int(days.astype(int) / 1)
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

        default = datetime.fromisoformat(default)

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
                start_date = default.isoformat()

        else:
            start_date = default.isoformat()

    return start_date


def get_bnds_variables(ds_id, ds):
    bnd_vars = ["latitude", "longitude", "time"]
    bounds_list = [ds.cf.get_bounds(bv).name for bv in bnd_vars]
    return bounds_list
