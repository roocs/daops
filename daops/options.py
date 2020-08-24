import os
import sys

from roocs_utils import config

project_base_dirs = config.project_base_dirs

if "ROOCS_CONFIG" in os.environ:
    config_path = os.environ["ROOCS_CONFIG"]
    sys.path.insert(1, config_path)
    import config_local as config
    project_base_dirs.update(config.project_base_dirs)


def get_project_base_dir(project):
    return project_base_dirs.get(project)

