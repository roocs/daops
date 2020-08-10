import os
import sys

if 'ROOCS_CONFIG' in os.environ:
    config_path = os.environ['ROOCS_CONFIG']
    sys.path.insert(1, config_path)
    import config_local as config

else:
    import roocs_utils.config as config

project_base_dirs = config.project_base_dirs