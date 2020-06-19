import importlib


def resolve_import(import_path):
    """
    Deconstructs path, imports module and returns callable.

    :param import path: module and function as 'x.y.func' (of any depth)
    :return: callable.
    """
    # Split last item off path
    parts = import_path.split('.')
    ipath = '.'.join(parts[:-1])
    func_name = parts[-1]

    # Import module then send the args and kwargs to the function
    try:
        module = importlib.import_module(ipath)
        func = getattr(module, func_name)
    except Exception as exc:
        raise ImportError(f'Could not import function from path: {import_path}')

    return func
