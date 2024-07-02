import os

from common import constants
import logging
from common.configuration import agent_config

# TODO
def test_main():
    import os
    os.geteuid = lambda: 0

    from cli import main
    #main.install_service()
    #assert os.path.exists('/'.join([agent_config.fs_root_path, constants.service_fn]))