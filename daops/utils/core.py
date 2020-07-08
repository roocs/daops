import collections
import importlib
import xarray as xr

from daops.utils import fixer


def _wrap_sequence(obj):
    if isinstance(obj, str):
        obj = [obj]
    return obj


def is_dataref_characterised(data_ref):
    return True


def is_characterised(data_refs, require_all=False):
    """
    Takes in an individual data reference or a sequence of them.
    Returns an ordered dictionary of data_refs with a boolean value
    for each stating whether the dataset has been characterised.

    If `require_all` is True: return a single Boolean value.

    :param data_refs: one or more data references
    :param require_all: Boolean to require that all must be characterised
    :return: Ordered Dictionary OR Boolean (if `require_all` is True)
    """
    data_refs = _wrap_sequence(data_refs)
    resp = collections.OrderedDict()

    for dref in data_refs:
        _is_char = is_dataref_characterised(dref)

        if require_all and not _is_char:
            return False

        resp[dref] = is_dataref_characterised(dref)

    return resp


def open_dataset(ds_id, file_paths):
    # Wrap xarray open with required args

    fix = fixer.Fixer(ds_id)
    if fix.pre_processor:
        for pre_process in fix.pre_processors:
            print(f'[INFO] Loading data with pre_processor: {pre_process.__name__}')
    else:
        print(f'[INFO] Loading data')

    ds = xr.open_mfdataset(file_paths, preprocess=fix.pre_processor,
                           use_cftime=True, combine='by_coords')

    if fix.post_processor:
        for post_process in fix.post_processor:
            func, args, kwargs = post_process
            print(f'[INFO] Running post-processing function: {func.__name__}')
            ds = func(ds, *args, **kwargs)

    return ds


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


class Fixer(object):

    def __init__(self, ds_id):
        self.ds_id = ds_id
        self.es = Elasticsearch(
            [f'es{i}.ceda.ac.uk' for i in range(9, 17)],
            use_ssl=True)
        # ca_certs='cert.pem',
        # port=9200)
        self._lookup_fix()

    def _convert_id(self, id):
        m = hashlib.md5()
        m.update(id.encode("utf-8"))
        return m.hexdigest()

    def _lookup_fix(self):
        id = self._convert_id(self.ds_id)
        content = es.get(index='roocs-fix', id=id)
        for fix in content["fixes"]:
            ref_implementation = fix["reference_implementation"]

        fix_file = os.path.join(self.FIX_DIR, f'{self.ds_id}.json')

        if not os.path.isfile(fix_file):
            self.pre_processor = None
            self.post_processor = None
            self.pre_processors = ()

        else:
            content = json.load(open(fix_file))
            pre_processors = content.get('pre_processors', None)
            post_processors = content.get('post_processors', None)

            if pre_processors:
                self.pre_processors = []
                for pre_processor in pre_processors:
                    self.pre_processors.append(resolve_import(pre_processor['func']))
            else:
                self.pre_processors = ()
            self.pre_processor = FuncChainer(self.pre_processors)

            if post_processors:
                post_process_list = []
                for post_processor in post_processors:
                    post_process_list.append((resolve_import(post_processor['func']),
                                              post_processor.get('args', None) or [],
                                              post_processor.get('kwargs', None) or {}))
                self.post_processor = post_process_list
            else:
                self.post_processor = ()