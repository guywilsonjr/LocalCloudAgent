import os
import shutil

from tests.common_test.test_fixtures import setup_file_system
from common.configuration import ensure_dirs_exist, validate_fs, agent_config


def test_ensure_dirs_exist():
    if os.path.exists(agent_config.metadata_dir):
        shutil.rmtree(agent_config.metadata_dir)
    if os.path.exists(agent_config.agent_dir):
        os.rmdir(agent_config.agent_dir)
    if os.path.exists(agent_config.operations_dir):
        os.rmdir(agent_config.operations_dir)

    ensure_dirs_exist()
    assert os.path.exists(agent_config.metadata_dir)
    assert os.path.exists(agent_config.agent_dir)
    assert os.path.exists(agent_config.operations_dir)


def test_validate_fs(setup_file_system):
    assert not os.path.exists(agent_config.repo_dir)
    os.makedirs(agent_config.repo_dir)
    with open(agent_config.aws_creds_fp, 'w') as f:
        f.write('')
    validate_fs()



def test_failing_validate_fs():
    return
