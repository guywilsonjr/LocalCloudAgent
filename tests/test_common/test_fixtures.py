import json
import logging
import os
import shutil

import pytest
from git import Repo

from agent.configuration import agent_config
from agent.versioning import VersionInfo
from common import constants


def rmfile(path):
    if os.path.exists(path):
        os.remove(path)


def rmdir(path):
    if os.path.exists(path):
        os.rmdir(path)


def rmtree(path):
    if os.path.exists(path):
        shutil.rmtree(path)



def create_test_repo():
    if not os.path.exists(agent_config.repo_dir):
        if 'LOCAL_CLOUD_AGENT_CONF_PATH' not in os.environ:
            raise RuntimeError('LOCAL_CLOUD_AGENT_CONF_PATH not set')
        Repo.clone_from(constants.repo_url, agent_config.repo_dir)


logging.info(f'Setting up test file system at: {agent_config.fs_root_path}')



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
@pytest.fixture(scope='session')
def setup_file_system():
    pending_dir_creations = {
        'LogDir': agent_config.log_dir,
        'HomeDir': agent_config.home_dir,
        'AwsDir': agent_config.aws_dir,
        'MetadataDir': agent_config.metadata_dir,
        'OperationsDir': agent_config.operations_dir,
        'AgentDir': agent_config.agent_dir
    }
    [os.makedirs(pendir, exist_ok=True) for pendir in pending_dir_creations.values()]
    create_test_repo()
    with open(agent_config.aws_creds_fp, 'w') as f:
        f.write('')

    with open(agent_config.agent_registration_fp, 'w') as f:
        f.write(
            json.dumps(
                {
                    'agent_id': test_agent_id,
                    'operations_queue_url': test_operations_queue_url,
                    'version': test_version,
                    'agent_key': test_agent_key, # TODO: This is not used in the agent
                    'ip_address': test_ip_address  # TODO: This is not used in the agent
                }
            )
        )
        f.write('\n')

    yield None
    rmtree(agent_config.fs_root_path)





