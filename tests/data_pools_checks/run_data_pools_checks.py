import os
os.environ["USE_PYGEOS"] = "0"
import random
import xarray as xr
import tempfile
import datetime
import numpy as np
import shutil
import time
import argparse

from daops.ops.subset import subset
from roocs_utils.xarray_utils.xarray_utils import open_xr_dataset
from roocs_utils.parameter.param_utils import time_interval, level_interval

from .results_db import ResultsDB
from .examples_data import data_pool_tests_db
from .caching import cached_output_fn, CachedResult


class SubsetTester:

    def __init__(self,
                 test_location='',
                 use_cache=True):

        self._test_location = test_location
        self._use_cache = use_cache
        self._tmpdir = None


    def main(self):

        results_db_columns = ['test_location', 'test_time', 'collection', 'area',
                              'level', 'time', 'success', 'message']    

        file_stem = f'tests_{self._test_location}'
        with ResultsDB(results_db_columns,
                       csvgz_file=f'{file_stem}.csv.gz',
                       sqlite_file=f'{file_stem}_tmp.db') as rdb:

            row_writer = lambda **kwargs: \
                rdb.add_row(test_location=self._test_location,
                            test_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                            **kwargs)

            for collection in data_pool_tests_db:
                self.test_subset_in_data_pools(collection, row_writer)


    def test_subset_in_data_pools(self, collection, row_writer=None):
        """
        Do a range of tests on a given collection
        """

        ds = self._open_dataset(collection)

        for test_kwargs, description in self._get_tests():

            print(description)
            subset_params, success, message = self._do_test(collection, ds, **test_kwargs)

            if row_writer is not None:
                self._store_result(row_writer,
                                  collection, subset_params, success, message)


    def _store_result(self, row_writer, collection, subset_params, success, message):
        tm = subset_params.get('time')
        if tm is not None:
            tm = '/'.join(str(v) for v in tm.value)
        level = subset_params.get('level')
        if level is not None:
            level = '/'.join(str(float(v)) for v in level.value)
        area = subset_params.get('area')
        if area is not None:
            area = '/'.join(str(v) for v in area)
        success = str(success)

        row_writer(collection=collection,
                   area=area,
                   level=level,
                   time=tm,
                   success=success,
                   message=message)


    def _get_tests(self):
        """
        Gets a sequence of tests to do.
        """

        # subset horizontally and in time
        for _ in range(3):
            yield {'do_area': True,
                   'do_time': True}, 'subset by area and time'

        # subset in all dimensions (though levels will be ignored if there isn't
        # a level dimension)
        for _ in range(3):
            yield {'do_area': True,
                   'do_time': True,
                   'do_levels': True}, 'subset by area, time and levels'

        # and a few special cases to try
        special_cases = [{"force_lon_wrap": True},
                         {"force_pole": "north"},
                         {"force_pole": "south"},
                         {"force_lon_wrap": True, "force_pole": "south"}]

        for area_args in special_cases:
            yield {'do_area': True,
                   'do_time': True,
                   'do_levels': True,
                   'area_args': area_args}, f"Doing special case: {area_args}"


    def _open_dataset(self, collection):

        print(f"opening {collection}")

        if collection[0] == "/":
            return xr.open_dataset(collection)

        #====================================
        ## THIS OUGHT TO WORK, but I need to work out how to configure the paths
        ## for the tests.  strace shows that it is using /tmp/roocs.ini but this
        ## is overwritten every time (tests/conftest.py gets imported and
        ## write_roocs_cfg() is run)
        ##
        ## strace also says that it is also looking in all of these:
        ##     <roocs_dir>/clisops/clisops/etc/roocs.ini
        ##     <roocs_dir>/daops/daops/etc/roocs.ini
        ##     <roocs_dir>/roocs-utils/roocs_utils/etc/roocs.ini
        ##
        ## For now, symlinking ~/.mini-esgf-data/master/test_data/badc
        ## to point to the real /badc will do for a workaround -- now it finds 
        ## the dataset
        ds = open_xr_dataset(collection)

        ## OR HERE IS ANOTHER POSSIBLE TEMPORARY WORKAROUND
        # import glob  # for open_xr_dataset workaround
        # assert isinstance(collection, str)
        #paths = glob.glob(f'/badc/cmip6/data/{collection.replace(".","/")}/*.nc')
        #ds = open_xr_dataset(paths)
        #====================================

        return ds


    def _dump_dims(self, ds, label=""):
        ignore = ("bnds", "vertices")
        print(f"{label} dataset dimensions: "
              f'{",".join(f"{k}:{v}" for k, v in ds.dims.items() if k not in ignore)}')


    def _get_data(self, val):
        return val.data if isinstance(val, (xr.DataArray, xr.IndexVariable)) else val


    def _do_test(self, collection, ds, **kwargs):
        """
        Do an individual test on a collection
        """

        print(f"Doing test on {collection} using {kwargs}")
        self._dump_dims(ds, label="input")
        subset_params, expect = self._prepare_test(ds, **kwargs)

        temp_dir = tempfile.TemporaryDirectory()
        self._tmpdir = temp_dir.name

        print("===========================================")
        print("Doing test with:")
        print(f"\n  Collection: {collection}")
        print("\n  Subset params:")
        for k, v in subset_params.items():
            if k == "time":
                v = f"time_interval({v.value})"
            elif k == "level":
                v = f"level_interval({tuple([float(lev) for lev in v.value])})"
            print(f"      {k} : {v}")
        print("\n  Expect to get:")
        for k, v in expect.items():
            if v is not None:
                print(f"      {k} : {self._get_data(v)}")
        if all(k in expect and expect[k] is None
               for k in ("lons_in_range", "lats_in_range")):
            print("  (curvilinear grid; will test lon/lat ranges, not exact vals)")

        print("\n===========================================")

        try:
            result = self._subset(collection, **subset_params)

            self._check_result(result, expect, collection, subset_params)

        except KeyboardInterrupt:
            raise
        except Exception as exc:
            success = False
            message = str(exc)
            self._print_error(f"TEST FAILED: {message}")
            raise  # FIXME: comment out
        else:
            success = True
            message = ""
            print("Test succeeded\n\n\n")
        finally:        
            temp_dir.cleanup()

        return subset_params, success, message


    def _print_error(self, message):
        stars = "*" * len(message)
        print(f"****{stars}****\n"
              f"*** {message} ***\n"
              f"****{stars}****\n\n\n")


    def _prepare_test(self, ds, do_area=False, do_time=False, do_levels=False, area_args=None):
        """
        returns the params to the subset function that will be needed for the test
        and a dictionary of things to expect to come back from the test

        The boolean inputs do_area, do_time, do_levels control whether to subset
        in each of these ways.  The input area_args can contain a dictionary of arguments
        to get_rand_area (ignored if do_area==False)
        """

        if area_args == None:
            area_args = {}

        params = {}
        expect = {}

        if do_area:
            area = self._get_rand_area(ds, **area_args)
            req_area = [float(v) for v in area["req_area"]]

            params["area"] = req_area

            expect["lons_in_range"] = area["lons_in_range"]
            expect["lats_in_range"] = area["lats_in_range"]
        else:
            expect["lons_in_range"] = self._get_lons(ds)
            expect["lats_in_range"] = self._get_lats(ds)

        if do_levels:
            lev_int = self._get_rand_lev_int(ds)
            if lev_int is not None:
                params["level"] = lev_int["req_interval"]
                expect["levs_in_range"] = lev_int["levs_in_range"]
            else:
                print("WARNING: not requesting level range as no level dimension found")
                expect["levs_in_range"] = None
        else:
            expect["levs_in_range"] = self._get_levs(ds)

        if do_time:
            time_int = self._get_rand_time_int(ds)
            if time_int is not None:
                params["time"] = time_int["req_interval"]
                expect["times_in_range"] = time_int["times_in_range"]
            else:
                print("WARNING: not requesting time range as no time dimension found")
                expect["times_in_range"] = None
        else:
            expect["times_in_range"] = self._get_times(ds)

        return params, expect


    def _get_rand_time_int(self, ds):
        """
        Returns a dictionary containing a randomly chosen time interval
        (in the form needed by the subset function) and the time values
        that would be expected when subsetting using that interval
        """
        times = self._get_times(ds)
        if times is None:
            return None
        t_start, t_end, vals_in_range = self._get_rand_range(times)
        ts_start = self._get_time_string(t_start)
        ts_end = self._get_time_string(t_end)
        return {"req_interval": time_interval(ts_start, ts_end),
                "times_in_range": vals_in_range}


    def _get_rand_lev_int(self, ds):
        """
        As get_rand_time_int, but for levels
        """
        levs = self._get_levs(ds)
        if levs is None:
            return None
        z_start, z_end, vals_in_range = self._get_rand_range(levs)
        return {"req_interval": level_interval(z_start, z_end),
                "levs_in_range": vals_in_range}


    def _get_time_string(self, when):
        """
        Turns a datetime, or time value seen in xarray,
        into a string understood by time_interval
        """
        if isinstance(when, datetime.datetime):
            t = when
        else:
            t = when.values.tolist()

        return (f"{t.year:04d}-{t.month:02d}-{t.day:02d}"
                f"T{t.hour:02d}:{t.minute:02d}:{t.second:02d}")


    def _get_rand_area(self, ds, force_lon_wrap=False, force_pole=None):
        """Returns a dictionary containing a randomly chosen area
        (tuple of lon_w, lat_s, lon_e, lat_n) and the lon and lat
        values that would be expected when subsetting using that area.

        In the curvilinear case (lon and lat variables in the file are 2d), the
        expected values will be None rather than arrays of expected values.  The
        reason for this is that it is not possible to validate a *specific* set of
        lon, lat values in any case (as although the subsetting will set any
        points that are out of range to NaN, but NaN values could also be because
        of missing data points within the range).
        """

        ## (lon0, lon1, lons_in_range), wrap_lon = self._get_rand_lon_range(ds)
        (lon0, lon1, lons_in_range) = self._get_rand_lon_range(ds, force_wrap=force_lon_wrap)
        (lat0, lat1, lats_in_range) = self._get_rand_lat_range(ds, force_pole=force_pole)

        return {"req_area": (lon0, lat0, lon1, lat1),
                "lons_in_range": lons_in_range,
                ## "wrap_lon": wrap_lon,
                "lats_in_range": lats_in_range}


    def _get_wrap_lon(self, lons):
        """
        Get the longitude at which the wrapping occurs.
        Note - the exact value is not used in the current version of the calling code,
        the main purpose here is to distinguish global from limited area, so that the
        requested area for subsetting does not wrap for a limited area grid.
        """
        minlon = lons.min()
        maxlon = lons.max()
        if maxlon - minlon < 270:
            # assume this is a limited area
            return None
        elif maxlon - minlon >= 360:
            raise Exception(f"too wide lon range {minlon} to {maxlon}")
        elif 0 <= minlon and maxlon < 360:
            return 360.
        elif -180 <= minlon and maxlon < 180:
            return 180.
        else:
            raise Exception(f"unsupported lon range {minlon} to {maxlon}")


    def _get_rand_lon_range(self, ds, force_wrap=False):
        """
        Get a randomly chosen longitude range.  This might include wrapping around
        (unless the longitudes don't seem to span global range), but if force_wrap is
        set to True then it ensures that this occurs.
        """
        lons = self._get_lons(ds)
        wrap_lon = self._get_wrap_lon(lons)
        can_wrap=(wrap_lon is not None)

        if force_wrap:
            print("WARNING: forcing longitude wrapping for what appears to be limited area model")
            params = {"force": "wrap"}
        else:
            params = {"can_wrap": can_wrap}
        return self._get_rand_range(lons, **params)


    def _get_rand_lat_range(self, ds, force_pole=None):
        """
        Get a randomly chosen latitude range.  If force_pole is set to "north" or "south",
        then the range will extend to the relevant pole.
        """

        lats = self._get_lats(ds)

        # using "force" will ensure that the range returned
        # by get_rand_range goes to the end of the latitude values,
        # but for the test, actually use -90 or 90. Which value is
        # to be overwritten will depend on the ordering. 
        # 
        if force_pole == "north":
            ret = self._get_rand_range(lats, force="upper")
            return (ret[0], 90., ret[2]) if ret[1] >= ret[0] else (90., ret[1], ret[2])
            params["force"] = "upper"        
        elif force_pole == "south":
            ret = self._get_rand_range(lats, force="lower")
            return (-90., ret[1], ret[2]) if ret[1] >= ret[0] else (ret[0], -90., ret[2])
        else:
            return self._get_rand_range(lats)


    def _get_rand_range(self, var, max_fraction=.1, can_wrap=False, force=None):
        """
        Get a random range from specified variable (which can be any number
        of dimensions).  Returns tuple of (lower, upper, values in range)

        min and max are chosen based on histogram of values, defaulting to returning
        a range that includes up to to about 10% of the points (though can be less)

        can_wrap=True means could be used with longitude - e.g. for a wrapping longitude of
        360 it could return lower=-10 upper=10, and the values in range are in the range -10 to 10
        where those values from -10 to 0 are based on the values from 350 to 360 in the input

        force can be used for special cases: "lower" forces the range to include
        the lower end (e.g. south pole for latitude), "upper" forces it to include
        the upper end (e.g. north pole), "wrap" forces it to wrap around (the meridian
        for longitude)
        """

        length = random.uniform(0, max_fraction)

        while True:

            did_wrap = False
            if force == "lower":
                lower_q = 0.
                upper_q = length
            elif force == "upper":
                lower_q = 1 - length
                upper_q = 1.            
            elif force == "wrap":
                lower_q = random.uniform(1 - length, 1)
                upper_q = lower_q + length - 1
                did_wrap = True
            elif force is not None:
                raise ValueError(f"unrecognised force value {force}")
            elif can_wrap:
                lower_q = random.uniform(0, 1)
                upper_q = lower_q + length
                did_wrap = upper_q > 1
                if did_wrap:
                    upper_q -= 1
            else:
                lower_q = random.uniform(0, 1 - length)    
                upper_q = lower_q + length

            lower = var.quantile(lower_q)
            upper = var.quantile(upper_q)

            if did_wrap:
                in_range = (lower <= var) | (var <= upper)
                if var.ndim == 1:
                    modulus = 360
                    lower_vals = self._get_data(var[lower <= var])
                    upper_vals = self._get_data(var[var <= upper])

                    if var.min() >= 0:
                        # data uses 0-360
                        # change e.g. 350..10 to -10..10
                        # (as subset function doesn't seem to like 350..370)
                        lower -= modulus
                        lower_vals -= modulus
                    else:
                        # data uses -180 to 180
                        # change e.g. 170..-170 to 170..190
                        upper += modulus
                        upper_vals += modulus

                    vals_in_range = np.concatenate((lower_vals, upper_vals))
                else:
                    vals_in_range = None
            else:
                in_range = (lower <= var) & (var <= upper)
                vals_in_range = var[in_range] if var.ndim == 1 else None

            if in_range.sum() > 0:
                break
            length = min(length * 2, 1)

        if var.ndim == 1 and len(var) > 1 and var[1] < var[0]:
            # if the variable is 1d and is decreasing, then swap the ordering
            # of the bounds (which were chosen based on histogram so will be increasing at this point)
            assert not did_wrap  # longitude wrap not verified for decreasing lons
            assert lower <= upper
            lower, upper = upper, lower

        return (lower, upper, vals_in_range)


    def _get_lons(self, ds):
        "Get the longitude variable for a dataset. Not necessarily a coordinate variable."
        return self._get_var_by_stdname(ds, "longitude")
    def _get_lats(self, ds):
        "Get the latitude variable for a dataset. Not necessarily a coordinate variable."
        return self._get_var_by_stdname(ds, "latitude")

    def _get_times(self, ds):
        "Get the time coordinate variable for a dataset"
        return self._get_axis_by_direction(ds, "T")
    def _get_levs(self, ds):
        "Get the height coordinate variable for a dataset"
        return self._get_axis_by_direction(ds, "Z")


    def _get_var_by_stdname(self, ds, stdname):
        """
        Get variable with a given standard name.
        Will raise an exception if there is not exactly one.
        """
        vars = [v for v in ds.variables.values()
                if v.attrs.get("standard_name") == stdname]
        var, = vars
        return var


    def _is_curvi(self, lons, lats):
        """
        Test whether given lon and lat variables correspond to a curvilinear grid
        (as opposed to 1d coordinate variables).
        """
        if len(lons.dims) == 1 and len(lats.dims) == 1:
            return False
        elif len(lons.dims) == 2 and lons.dims == lats.dims:
            return True
        else:
            raise Exception(f"unexpected dimensionality of lon, lat arrays: {lon.dims} and {lat.dims}")


    def _get_gridded_vars(self, ds, lons=None, lats=None, curvi=None):
        if lons is None:
            lons = self._get_lons(ds)
        if lats is None:
            lats = self._get_lats(ds)
        if curvi is None:
            curvi = self._is_curvi(lons, lats)

        if curvi:
            grid_dims = lons.dims
        else:
            latdim, = lats.dims
            londim, = lons.dims
            grid_dims = (latdim, londim)
        return [v for v in ds.data_vars.values()
                if v.dims[-2:] == grid_dims]


    def _get_lonlat_ranges_for_curvi(self, ds):
        """
        get ranges of lon, lat values where there is actual data (not masked)
        for any variable on the lon, lat grid
        """

        lons = self._get_lons(ds)
        lats = self._get_lats(ds)

        grid_shape = lons.shape

        # get a list of the variables that are on the lon-lat grid,
        # other than lon, lat themselves, and then get an array of 
        # positions where there are non-NaN values in *any* of these 
        # variables, for any other level / height
        #
        # (start with 2d array of False, then use logical OR with 
        # each variable, although probably there is only one such var)
        #
        vars_on_grid = self._get_gridded_vars(ds,
                                             lons=lons, lats=lats,
                                             curvi=True)
        if not vars_on_grid:
            raise Exception("could not find any data variables")
        has_data = np.zeros(grid_shape, dtype=bool)
        for var in vars_on_grid:
            var_has_data = np.logical_not(np.isnan(var.data))        
            # reduce to 2d using "any" in loop - there might be a cleverer way
            while var_has_data.ndim > 2:
                var_has_data = np.any(var_has_data, axis=(var_has_data.ndim - 3))
            assert var_has_data.shape == grid_shape
            has_data |= var_has_data

        if not has_data.any():
            print ("WARNING: data variable(s) contain only NaN values")
            return (None, None)

        lons_where_data = lons.data[has_data]
        lats_where_data = lats.data[has_data]

        lon_range_where_data = (lons_where_data.min(), lons_where_data.max())
        lat_range_where_data = (lats_where_data.min(), lats_where_data.max())

        print("For this curvilinear dataset:")
        print(f" Lon range where data {lon_range_where_data} "
              f"(overall {lons.data.min(), lons.data.max()})")
        print(f" Lat range where data {lat_range_where_data} "
              f"(overall {lats.data.min(), lats.data.max()})")

        return (lon_range_where_data, lat_range_where_data)


    def _check_in_range(self, actual_range, requested_range, label="", **kwargs):
        """
        check whether the range of values lies WITHIN the requested range of values;
        allow for the fact that the requested range might be passed in decreasing order
        """
        if not self._is_in_range(actual_range, requested_range, **kwargs):
            raise Exception(f"range check for {label} failed")
        print(f"{label}: Verified range {actual_range} within {requested_range}")


    def _is_in_range(self, actual_range, requested_range):
        """
        helper for check_in_range.  Returns boolean.
        """
        req0, req1 = requested_range
        if req0 > req1:
            req0, req1 = req1, req0
        return all((req0 <= val <= req1
                    for val in actual_range))


    def _check_equal(self, vals, exp_vals, label=""):
        """
        Check whether the values match the expected values
        """

        vals = self._get_data(vals)
        exp_vals = self._get_data(exp_vals)

        #print(f"\n\n============ {label} =========\n\n")
        #print(f"Actual vals: {vals}")
        #print(f"Expected vals: {exp_vals}")

        if not np.array_equal(vals, exp_vals):
            raise Exception(f"equal values assertion failed for {label}:"
                            f"actual {vals}, expected: {exp_vals}")

        print(f"{label}: checked {len(vals)} values match expected values")


    def _check_result(self, result, expect, collection, subset_params):

        """
        Do various checks on the result of subsetting.  result should be an
        object that has a file_uris property.  expect should be dictionary
        returned by prepare_test.

        subset_params is the dictionary of keyword args that was passed to
        subset (needed for curvilinear - see below).

        Currently, the tests that are done are:
        - check that the exact set of coordinate values matches what was expected,
        - except that in the case of a curvilinear grid, check to see what lon and
          lat ranges are spanned by the lon and lat arrays in the file but only
          including those locations where there is data with non-NaN values; then
          check that these are within the range that was requested
        """

        fn, = result.file_uris
        dsout = xr.open_dataset(fn)
        self._dump_dims(dsout, label="output")

        lons = self._get_lons(dsout)
        lats = self._get_lats(dsout)

        curvi = self._is_curvi(lons, lats)

        if curvi and "area" in subset_params:
            area = subset_params["area"]
            req_lon_range = (area[0], area[2])
            req_lat_range = (area[1], area[3])

            lon_range, lat_range = self._get_lonlat_ranges_for_curvi(dsout)
            if lon_range is not None:
                print("Checking that lon-lat values with (unmasked) data in requested range")
                self._check_in_range(lon_range, req_lon_range, label="longitudes")
                self._check_in_range(lat_range, req_lat_range, label="latitudes")
            else:
                print("Skipping lon/lat range check: did not find any data in requested range")
        else:
            expected_lons = expect["lons_in_range"]
            expected_lats = expect["lats_in_range"]

            self._check_equal(lons, expected_lons, label="longitudes")
            self._check_equal(lats, expected_lats, label="latitudes")

        expected_levs = expect["levs_in_range"]
        if expected_levs is not None:
            levs = self._get_levs(dsout)   
            self._check_equal(levs, expected_levs, label="levels")

        expected_times = expect["times_in_range"]
        if expected_times is not None:
            times = self._get_times(dsout)
            self._check_equal(times, expected_times, label="times")
            timeval = times[0]
        else:
            timeval = None

        vars_on_grid = self._get_gridded_vars(dsout,
                                             lons=lons, lats=lats,
                                             curvi=curvi)

        self._do_nans_check(vars_on_grid, collection, timeval)


    def _get_axis_by_direction(self, ds, direction):
        """
        Get the axis with the specified direction attribute ("X", "Y", "Z" or "T")
        or if there is none, returns None.
        (If more than one, raises an exception.)
        """
        axes = []
        for name in ds.dims:
            axis = ds[name]
            if name == "bnds":
                continue
            if hasattr(axis, "axis") and axis.axis == direction:
                axes.append(axis)
        if len(axes) > 1:
            raise Exception(f"more than one dimension with axis {direction}")
        elif len(axes) == 1:
            return axes[0]
        else:
            return None


    def _do_nans_check(self, vars_on_grid, collection, timeval):
        """
        Check whether any of the variables consist of all NaN values.
        If so, then extract (for one timestep) the variable on all grid points.
        If that variable consists of some but not all NaN values, then assume 
        that the subsetter is working and we are just requesting a region where
        there are NaN values, so downgrade to a warning -- otherwise raise
        an exception.
        """

        vars_with_nans = set()
        for var in vars_on_grid:
            if np.all(np.isnan(var.data)):
                vars_with_nans.add(var.name)

        if vars_with_nans:
            dsout2 = self._get_fullfield(collection, timeval=timeval)

            for varname in vars_with_nans:
                isnan_ref = np.isnan(dsout2[varname].data)
                if np.any(isnan_ref) and not np.all(isnan_ref):
                    print(f"Warning: {varname} contains all NaNs (but some non-NaNs exist in full field).")
                else:
                    raise Exception(f"Variable {varname} contains all NaNs.")


    def _subset(self, collection, **subset_params):

        if self._use_cache:
            cached_fn = cached_output_fn(collection, subset_params)
            if os.path.exists(cached_fn):
                print(f"using cache: {cached_fn}")
                result = CachedResult(cached_fn)           
            else:
                result = subset(collection,
                                output_dir=self._tmpdir,
                                **subset_params)
                fn, = result.file_uris
                print(f"caching: {cached_fn}")            
                shutil.copy(fn, cached_fn)
        else:
            result = subset(collection,
                            output_dir=self._tmpdir,
                            **subset_params)
        return result


    def _get_fullfield(self, collection, timeval=None):
        """
        Get the result of subsetting, optionally by time to a particular
        time value, but not in any other dimensions.
        """    
        params = {}
        if timeval is not None:
            t_iso = timeval.data.tolist().isoformat()
            params['time'] = time_interval(t_iso, t_iso)

        result = self._subset(collection, **params)
        fn, = result.file_uris
        return xr.open_dataset(fn)


def _cli_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('test_location',
                        help='test location, e.g. CEDA')
    parser.add_argument('--seed', '-s', type=int,
                        help='value for random seed')
    parser.add_argument('--cache', '-c', action='store_true',
                        help='use cache of subsetter output')
    return parser.parse_args()


def cli():
    args = _cli_arg_parser()
    if args.seed is not None:
        random.seed(args.seed)
    else:
        if args.cache:
            print('Warning: using --cache but not --seed; cache hits are unlikely.')
    tester = SubsetTester(test_location=args.test_location,
                          use_cache=args.cache)
    tester.main()
    
