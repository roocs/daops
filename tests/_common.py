import os
import tempfile

from jinja2 import Template

TESTS_HOME = os.path.abspath(os.path.dirname(__file__))
TESTS_OUTPUTS = os.path.join(TESTS_HOME, "_outputs")
ROOCS_CFG = os.path.join(tempfile.gettempdir(), "roocs.ini")

try:
    os.mkdir(TESTS_OUTPUTS)
except Exception:
    pass


def write_roocs_cfg():
    cfg_templ = """
    [project:cmip5]
    base_dir = {{ base_dir }}/mini-esgf-data/test_data/badc/cmip5/data

    [project:cmip6]
    base_dir = {{ base_dir }}/mini-esgf-data/test_data/badc/cmip6/data

    [project:cordex]
    base_dir = {{ base_dir }}/mini-esgf-data/test_data/badc/cordex/data

    [project:c3s-cmip5]
    base_dir = {{ base_dir }}/mini-esgf-data/test_data/group_workspaces/jasmin2/cp4cds1/vol1/data

    [project:c3s-cmip6]
    base_dir = NOT DEFINED YET

    [project:c3s-cordex]
    base_dir = {{ base_dir }}/mini-esgf-data/test_data/group_workspaces/jasmin2/cp4cds1/vol1/data
    """
    cfg = Template(cfg_templ).render(base_dir=TESTS_HOME)
    with open(ROOCS_CFG, "w") as fp:
        fp.write(cfg)
    # point to roocs cfg in environment
    os.environ["ROOCS_CONFIG"] = ROOCS_CFG
