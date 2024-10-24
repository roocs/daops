"""Module to dispatch the processing operation to the correct mode (serial or parallel)."""

from loguru import logger


def dispatch(operation, dset, **kwargs):
    """Dispatch the operation to the correct mode (serial or parallel)."""
    logger.info("NOW SENDING TO PARALLEL DISPATCH MODE...")
    return process(operation, dset, mode="serial", **kwargs)


def process(operation, dset, mode="serial", **kwargs):
    """Run the processing operation on the dataset in the correct mode (in series or parallel)."""
    op_name = operation.__name__

    if mode == "serial":
        logger.info(f"Running {op_name} [{mode}]: on Dataset with args: {kwargs}")

        result = operation(dset, **kwargs)
    #        try:
    #            result = operation(dset, **kwargs)
    #        except Exception as err:
    #            raise Exception(f'Operation failed: {op_name} on {dset} with args: {kwargs}')
    else:
        result = dispatch(operation, dset, **kwargs)

    return result
