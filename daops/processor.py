from loguru import logger


def dispatch(operation, dset, **kwargs):
    logger.info(f"NOW SENDING TO PARALLEL DISPATCH MODE...")
    return process(operation, dset, mode="serial", **kwargs)


def process(operation, dset, mode="serial", **kwargs):
    """Runs the processing operation on the dataset in the correct mode (in series or parallel)."""

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
