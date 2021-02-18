from daops import logging
from daops.utils import normalise


LOGGER = logging.getLogger(__file__)


def dispatch(operation, dset, **kwargs):
    LOGGER.info(f"NOW SENDING TO PARALLEL DISPATCH MODE...")
    return process(operation, dset, mode="serial", **kwargs)


def process(operation, dset, mode="serial", **kwargs):
    """ Runs the processing operation on the dataset in the correct mode (in series or parallel)."""

    op_name = operation.__name__

    if mode == "serial":
        LOGGER.info(f"Running {op_name} [{mode}]: on Dataset with args: {kwargs}")

        result = operation(dset, **kwargs)
    #        try:
    #            result = operation(dset, **kwargs)
    #        except Exception as err:
    #            raise Exception(f'Operation failed: {op_name} on {dset} with args: {kwargs}')
    else:
        result = dispatch(operation, dset, **kwargs)

    return result


def calculate(operation, **kwargs):

    collection = kwargs.pop("collection")
    apply_fixes = kwargs.pop("apply_fixes")

    # Normalise (i.e. "fix") data inputs based on "character"
    norm_collection = normalise.normalise(collection, apply_fixes)

    rs = normalise.ResultSet(vars())
    # change name of data ref here
    for dset, norm_collection in norm_collection.items():
        # Process each input dataset (either in series or
        # parallel)
        rs.add(
            dset,
            process(
                operation,
                norm_collection,
                **kwargs,
            ),
        )

    return rs
