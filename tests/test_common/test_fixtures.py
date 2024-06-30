import importlib
import json
import logging
import os
import shutil
import tempfile

import pytest
from git import Repo

from agent.versioning import VersionInfo
from common import constants


if 'LOCAL_CLOUD_AGENT_CONF_PATH' not in os.environ:
    raise RuntimeError('LOCAL_CLOUD_AGENT_CONF_PATH not set')


def rmfile(path):
    if os.path.exists(path):
        os.remove(path)


def rmdir(path):
    if os.path.exists(path):
        os.rmdir(path)


def rmtree(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def create_test_repo(test_fs_dir: str):
    test_repo_dir = f'{test_fs_dir}{constants.installed_repo_dir}'
    if not os.path.exists(test_repo_dir):
        logging.info(f'Creating test repo at: {test_repo_dir}')
        Repo.clone_from(constants.repo_url, test_repo_dir)


test_agent_id = 'test-agent-id'
test_operations_queue_url = 'https://sqs.us-west-1.amazonaws.com/012345678901/test'
test_agent_key = 'test-agent-key'
test_ip_address = '000.000.000.000'
test_major_version = 0
test_minor_version = 0
test_patch_version = 0
test_rc_version = 10
test_version_info = VersionInfo(
    major=test_major_version,
    minor=test_minor_version,
    patch=test_patch_version,
    release_candidate=test_rc_version
)
test_version = str(test_version_info)


# Note typical installation includes systemd service file, which is not included in this test setup
@pytest.fixture
def setup_file_system():
    with tempfile.TemporaryDirectory(delete=False) as tempdir:
        corrected_tempdir = tempdir[:-1]
        import common.configuration
        os.environ['FS_ROOT_PATH'] = corrected_tempdir
        common.configuration.AgentConfig.fs_root_path = corrected_tempdir
        importlib.reload(common.configuration)
        logging.info(f'Setting up test file system at: {common.configuration.agent_config.fs_root_path}')
        pending_dir_creations = {
            'LogDir': common.configuration.agent_config.log_dir,
            'HomeDir': common.configuration.agent_config.home_dir,
            'AwsDir': common.configuration.agent_config.aws_dir,
            'MetadataDir': common.configuration.agent_config.metadata_dir,
            'OperationsDir': common.configuration.agent_config.operations_dir,
            'AgentDir': common.configuration.agent_config.agent_dir
        }
        [os.makedirs(pendir, exist_ok=True) for pendir in pending_dir_creations.values()]
        create_test_repo(corrected_tempdir)
        with open(common.configuration.agent_config.aws_creds_fp, 'w') as f:
            f.write('')

        with open(common.configuration.agent_config.agent_registration_fp, 'w') as f:
            f.write(
                json.dumps(
                    {
                        'agent_id': test_agent_id,
                        'operations_queue_url': test_operations_queue_url,
                        'version': test_version,
                        'agent_key': test_agent_key,  # TODO: This is not used in the agent
                        'ip_address': test_ip_address  # TODO: This is not used in the agent
                    }
                )
            )
            f.write('\n')

        yield None

