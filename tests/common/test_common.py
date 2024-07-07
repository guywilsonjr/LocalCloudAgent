import pytest


@pytest.mark.usefixtures("root_fakefs", "fake_base_fs", "installed", "registered_agent")
def test_common():
    from common import constants
    from common import systemd