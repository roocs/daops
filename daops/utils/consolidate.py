import collections
import glob
import xarray as xr

from daops.utils.core import _wrap_sequence


def _consolidate_data_ref(dref, data_root_dir=None):
    if dref[0] == '/':
        return dref

    if dref.find('cmip5') > -1 and data_root_dir is not None:
        dref = data_root_dir.rstrip('/') + '/' + dref.replace('.', '/') + '/*.nc'

    return dref


def consolidate(data_refs, data_root_dir, **kwargs):
    data_refs = _wrap_sequence(data_refs)
    filtered_refs = collections.OrderedDict()

    for dref in data_refs:

        consolidated = _consolidate_data_ref(dref, data_root_dir)

        if 'time' in kwargs:
            required_years = set(range(*[int(_.split('-')[0]) for _ in kwargs['time']]))

            file_paths = glob.glob(consolidated)
            print(f'[INFO] Testing {len(file_paths)} files in time range: ...')
            files_in_range = []

            for i, fpath in enumerate(file_paths):
                print(f'[INFO] File {i}: {fpath}')
                ds = xr.open_dataset(fpath)

                found_years = set([int(_) for _ in ds.time.dt.year])

                if required_years.intersection(found_years):
                    files_in_range.append(fpath)

            print(f'[INFO] Kept {len(files_in_range)} files')
            consolidated = files_in_range[:]

        filtered_refs[dref] = consolidated

    return filtered_refs
