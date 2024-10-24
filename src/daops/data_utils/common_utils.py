from pydoc import locate


def handle_derive_str(value, ds_id, ds):
    if isinstance(value, str) and "derive" in value:
        components = value.split(":")
        func = locate(components[1].strip())
        if len(components) > 2:
            arg = value.split(":")[-1].strip()
            return func(ds_id, ds, arg)
        else:
            return func(ds_id, ds)
    else:
        return value
