import os

import pytest

from common.configuration import agent_config


@pytest.mark.usefixtures("root_fakefs", "fake_base_fs", "installed", "registered_agent")
def test_main() -> None:
    from cli import main
    main.install_service()
    assert os.path.exists(agent_config.installed_service_fp)

