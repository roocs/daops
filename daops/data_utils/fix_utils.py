def get_lead_times(ds, start_date):
    times = ds.time.values.astype("datetime64[ns]")
    reftime = np.datetime64(start_date)
    lead_times = []

    # calculate leadtime from reftime and valid times
    for time in times:
        td = time - reftime
        days = td.astype("timedelta64[D]")
        days = int(days.astype(int) / 1)
        lead_times.append(days)

    # put the lead times into a string format
    lts = ""
    for lt in lead_times:
        lts += f"{lt},"

    return lts.rstrip(",")


def get_start_date(ds, default=None):
    if not default:
        year = ds_id.split(".")[5].split("-")[0].lstrip("s")
        default = datetime(int(year), 11, 1, 0, 0).isoformat()

    sd = datetime.fromisoformat(default)
    start_date = f"s{sd.year}{sd.month}"
    return start_date


def get_reftime(ds, default=None):
    if not default:
        raise Exception(
            "default date must be provided in the format YYYY-MM-DDThh:mm:ss"
        )

    # get the start date

    start_date = ds.attrs.get("startdate", None)

    if not start_date:
        start_date = default

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
