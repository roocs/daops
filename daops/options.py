import os
import sys



project_base_dirs = {
    'cmip5': '/badc/cmip5/data',
    'cmip6': '/badc/cmip6/data',
    'cordex': '/badc/cordex/data',
    'c3s-cmip5': '/group_workspaces/jasmin2/cp4cds1/vol1/data/',
    'c3s-cmip6': 'NOT DEFINED YET',
    'c3s-cordex': '/group_workspaces/jasmin2/cp4cds1/vol1/data/'
}


def get_project_base_dir(project):
    return project_base_dirs.get(project)

