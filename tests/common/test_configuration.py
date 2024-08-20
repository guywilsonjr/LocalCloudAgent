import importlib
import os
import shutil

import pytest


def test_with_logging() -> None:
    os.makedirs('/var/log/local_cloud_agent', exist_ok=True)

    import local_cloud_agent.common.configuration
    importlib.reload(local_cloud_agent.common.configuration)

def test_logger_dir() -> None:
    os.makedirs('/var/log/local_cloud_agent', exist_ok=True)
    from local_cloud_agent.common.configuration import agent_config
    assert agent_config.log_dir == '/var/log/local_cloud_agent'
    shutil.rmtree('/var/log/local_cloud_agent')


def test_ensure_dirs_exist() -> None:
    from local_cloud_agent.common.configuration import ensure_dirs_exist, agent_config
    if os.path.exists(agent_config.metadata_dir):
        shutil.rmtree(agent_config.metadata_dir)
    assert not os.path.exists(agent_config.metadata_dir)
    ensure_dirs_exist()
    assert os.path.exists(agent_config.metadata_dir)
    assert os.path.exists(agent_config.agent_dir)
    assert os.path.exists(agent_config.operations_dir)


def test_validate_fs() -> None:
    from local_cloud_agent.common.configuration import validate_fs
    os.makedirs('/root/.aws', exist_ok=True)
    with open('/root/.aws/credentials', 'w') as f:
        f.write('')
    validate_fs()

    os.remove('/root/.aws/credentials')
    shutil.rmtree('/root')


def test_fail_validate_fs() -> None:
    from local_cloud_agent.common.configuration import validate_fs
    with pytest.raises(RuntimeError):
        validate_fs()

