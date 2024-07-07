import os

import pytest

from common.configuration import ensure_dirs_exist, validate_fs, agent_config


@pytest.mark.usefixtures("root_fakefs", "fake_base_fs", "aws")
def test_ensure_dirs_exist():
    assert not os.path.exists(agent_config.metadata_dir)
    ensure_dirs_exist()
    assert os.path.exists(agent_config.metadata_dir)
    assert os.path.exists(agent_config.agent_dir)
    assert os.path.exists(agent_config.operations_dir)


@pytest.mark.usefixtures("root_fakefs", "fake_base_fs", "installed")
def test_validate_fs():
    assert not os.path.exists(agent_config.repo_dir)
    os.makedirs(agent_config.repo_dir)
    with open(agent_config.aws_creds_fp, 'w') as f:
        f.write('')
    validate_fs()


