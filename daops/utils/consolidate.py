import collections
import glob
import xarray as xr

from daops.utils.core import _wrap_sequence


def _consolidate_data_ref(data_ref, project=None, base_dir=None):
    if data_ref[0] == "/":
        return data_ref

    if data_ref.find(project) > -1 and base_dir is not None:
        data_ref = base_dir.rstrip("/") + "/" + data_ref.replace(".", "/") + "/*.nc"

    return data_ref


def consolidate(collection, project, base_dir, **kwargs):
    collection = _wrap_sequence(collection)

    filtered_refs = collections.OrderedDict()

    for data_ref in collection:

        consolidated = _consolidate_data_ref(data_ref, project, base_dir)

        if "time" in kwargs:
            # need int(_.split('-')[0] if passing in more than year from TimeParameter
            required_years = set(range(*[int(_) for _ in kwargs["time"]]))

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
                raise Exception(f"No files found in given time range for {data_ref}")

        filtered_refs[data_ref] = consolidated

    return filtered_refs
