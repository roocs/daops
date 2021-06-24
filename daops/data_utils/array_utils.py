import xarray as xr
from roocs_utils.xarray_utils import xarray_utils as xu


def replace_lat_and_lon_fill_values(ds, **operands):

    # get the value to mask
    value = operands.get("value")
    # convert from string to number - value must be provided as a string (to work with elasticsearch)
    if isinstance(value, str):
        value = float(value)

    # gets latitude and longitude
    lat = xu.get_coord_by_type(ds, "latitude", ignore_aux_coords=False).name
    lon = xu.get_coord_by_type(ds, "longitude", ignore_aux_coords=False).name

    # if they are coordinate variables - don't fix
    for coord_id in lat, lon:
        if ds.coords[coord_id].dims == (coord_id,):
            return ds

    # make nans
    # ds[lat] = ds[lat].where(ds[lat] != value)
    # ds[lon] = ds[lon].where(ds[lon] != value)

    # or change fill value and set encoding for fill value
    ds[lat] = ds[lat].where(ds[lat] != value, 1e20)
    ds[lon] = ds[lon].where(ds[lon] != value, 1e20)
    ds[lat].encoding["_FillValue"] = 1e20
    ds[lon].encoding["_FillValue"] = 1e20

    return ds
