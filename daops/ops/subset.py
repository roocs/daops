from clisops.ops.subset import subset as clisops_subset
from roocs_utils.parameter import parameterise

from daops.processor import process
from daops.utils import consolidate
from daops.utils import normalise

__all__ = [
    "subset",
]


def subset(
    collection,
    time=None,
    area=None,
    level=None,
    output_dir=None,
    output_type="netcdf",
    split_method="time:auto",
    file_namer="standard",
):
    """
    Subset input dataset according to parameters.
    Can be subsetted by level, area and time.

    Parameters
    ----------
    collection: Collection of datasets to process, sequence or string of comma separated dataset identifiers.
    time: Time period - Time range to subset over, sequence of two time values or string of two / separated time values
    area: Area to subset over, sequence or string of comma separated lat and lon bounds. Must contain 4 values.
    level: Level range - Level values to subset over, sequence of two level values or string of two / separated level values
    output_dir: str or path like object describing output directory for output files.
    output_type: {"netcdf", "nc", "zarr", "xarray"}
    split_method: {"time:auto"}
    file_namer: {"standard", "simple"}

    Returns
    -------
    List of outputs in the selected type: a list of xarray Datasets or file paths.


    Examples
    --------
    | collection: ("cmip6.ukesm1.r1.gn.tasmax.v20200101",)
    | time: ("1999-01-01T00:00:00", "2100-12-30T00:00:00")
    | area: (-5.,49.,10.,65)
    | level: (1000.,)
    | output_type: "netcdf"
    | output_dir: "/cache/wps/procs/req0111"
    | split_method: "time:decade"
    | file_namer: "facet_namer"

    """

    parameters = parameterise(collection=collection, time=time, area=area, level=level)

    # Consolidate data inputs so they can be passed to Xarray

    collection = consolidate.consolidate(
        parameters.get("collection"), time=parameters.get("time")
    )

    # Normalise (i.e. "fix") data inputs based on "character"
    norm_collection = normalise.normalise(collection)

    rs = normalise.ResultSet(vars())
    # change name of data ref here
    for dset, norm_collection in norm_collection.items():

        # Process each input dataset (either in series or
        # parallel)
        rs.add(
            dset,
            process(
                clisops_subset,
                norm_collection,
                **{
                    "time": parameters.get("time"),
                    "area": parameters.get("area"),
                    "level": parameters.get("level"),
                    "output_type": output_type,
                    "output_dir": output_dir,
                    "split_method": split_method,
                    "file_namer": file_namer,
                },
            ),
        )

    return rs
