import collections
import glob
import xarray as xr

from daops.utils.core import _wrap_sequence
from daops.options import get_project_base_dir


def _consolidate_dset(dset):

    if dset[0] == "/":
        return dset

    project = dset.split('.')[0]
    base_dir = get_project_base_dir(project)

    if base_dir is not None:
        dset = base_dir.rstrip("/") + "/" + dset.replace(".", "/") + "/*.nc"

    return dset


def consolidate(collection, **kwargs):
    collection = _wrap_sequence(collection.tuple)

    filtered_refs = collections.OrderedDict()

    for dset in collection:
        consolidated = _consolidate_dset(dset)

        if "time" in kwargs:
            time = kwargs["time"].tuple
            # need int(_.split('-')[0] if passing in more than year from TimeParameter
            required_years = set(range(*[int(_) for _ in time]))

            file_paths = glob.glob(consolidated)
            print(f"[INFO] Testing {len(file_paths)} files in time range: ...")
            files_in_range = []

            for i, fpath in enumerate(file_paths):
                print(f"[INFO] File {i}: {fpath}")
                ds = xr.open_dataset(fpath)

                found_years = set([int(_) for _ in ds.time.dt.year])

                if required_years.intersection(found_years):
                    files_in_range.append(fpath)

            print(f"[INFO] Kept {len(files_in_range)} files")
            consolidated = files_in_range[:]
            if len(files_in_range) == 0:
                raise Exception(f"No files found in given time range for {dset}")

        filtered_refs[dset] = consolidated

    return filtered_refs
