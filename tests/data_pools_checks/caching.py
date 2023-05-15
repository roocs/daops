import os
import hashlib


def cached_output_fn(collection, params, odir=None):
    if odir == None:
        odir = '/tmp/roocs' ## FIXME
    if not os.path.isdir(odir):
        os.mkdir(odir)
    vals = [collection]
    if 'area' in params:
        vals.append('area')
        vals.extend(params['area'])
    if 'time' in params:
        vals.append('time')
        vals.extend(list(params['time'].value))
    if 'level' in params:
        vals.append('level')
        vals.extend(list(float(lev) for lev in params['level'].value))
    vals = tuple(vals)
    h = hashlib.sha1(str(vals).encode()).hexdigest()
    #print(f'CACHE FOR: {vals} => {h}')
    return f'{odir}/cache-{h}.nc'


class CachedResult:
    def __init__(self, path):
        self.file_uris = [path]
