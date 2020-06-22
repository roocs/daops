import clisops.ops

from daops.processor import process
from daops.utils import consolidate, normalise


def subset(data_refs, time=None, space=None, level=None,
           data_root_dir=None, output_dir=None,
           chunk_rules=None, filenamer=None):
    """
    Example:
        data_refs: ("cmip6.ukesm1.r1.gn.tasmax.v20200101",)
        time: ("1999-01-01T00:00:00", "2100-12-30T00:00:00")
        space: (-5.,49.,10.,65)
        level: (1000.,)
        output_type: "netcdf"
        output_dir: "/cache/wps/procs/req0111"
        chunk_rules: "time:decade"
        filenamer: "facet_namer"


    :param data_refs:
    :param time:
    :param space:
    :param level:
    :param output_dir:
    :param chunk_rules:
    :param filenamer:
    :return:
    """
    # Consolidate data inputs so they can be passed to Xarray
    data_refs = consolidate.consolidate(data_refs, time=time,
                                        data_root_dir=data_root_dir)
    # Normalise (i.e. "fix") data inputs based on "character"
    norm_dsets = normalise.normalise(data_refs)

    rs = normalise.ResultSet(vars())

    for data_ref, norm_dset in norm_dsets.items():

        # Process each input dataset (either in series or
        # parallel)
        rs.add(
            data_ref,
            process(
                clisops.ops.subset, norm_dset, **{
                    'time': time,
                    'space': space,
                    'level': level,
                    'output_type': 'netcdf',
                    'output_dir': output_dir,
                    'chunk_rules': chunk_rules,
                    'filenamer': filenamer
                }
            )
        )

    return rs
