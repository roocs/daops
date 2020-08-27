from clisops import utils


def double_array(da):
    var_id = utils.get_coords.get_main_variable(da)
    da[var_id].data = da[var_id].data * 2
    return da


def change_lat_name(da):
    da_update_lat_name = da.rename({"lat": "silly_lat"})
    return da_update_lat_name
