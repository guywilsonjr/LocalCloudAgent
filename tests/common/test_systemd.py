import subprocess

import pytest


def test_systemd(mocker):
    from local_cloud_agent.common import systemd
    systemd.reload_systemd()
    mocker.patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'cmd'))
    with pytest.raises(RuntimeError):
        systemd.reload_systemd()

