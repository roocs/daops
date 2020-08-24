import collections
import glob
import xarray as xr

from daops.utils.core import _wrap_sequence
from daops.options import get_project_base_dir


def _consolidate_col(col, project=None, base_dir=None):
    if col[0] == "/":
        return col

    if col.find(project) > -1 and base_dir is not None:
        col = base_dir.rstrip("/") + "/" + col.replace(".", "/") + "/*.nc"

    return col


def consolidate(collection, project, **kwargs):
    collection = _wrap_sequence(collection.tuple)

    filtered_refs = collections.OrderedDict()

    base_dir = get_project_base_dir(project)

    for col in collection:

        consolidated = _consolidate_col(col, project, base_dir)

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
                raise Exception(f"No files found in given time range for {col}")

        filtered_refs[col] = consolidated

    return filtered_refs
