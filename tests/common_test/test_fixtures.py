import json
import logging
import os
import common.configuration
import pyfakefs.fake_filesystem
from typing import Generator

import pytest

from common import constants
from tests.common_test import test_constants
from conftest import fake_filesystem


# Note typical installation includes systemd service file, which is not included in this test setup
@pytest.fixture(scope='function')
def setup_file_system(fake_filesystem: pyfakefs.fake_filesystem.FakeFilesystem) -> Generator[None, None, None]:
    pending_dir_creations = {
        'LogDir': common.configuration.agent_config.log_dir,
        'HomeDir': common.configuration.agent_config.home_dir,
        'AwsDir': common.configuration.agent_config.aws_dir,
        'MetadataDir': common.configuration.agent_config.metadata_dir,
        'OperationsDir': common.configuration.agent_config.operations_dir,
        'AgentDir': common.configuration.agent_config.agent_dir
    }
    [os.makedirs(pendir, exist_ok=True) for pendir in pending_dir_creations.values()]
    logging.info(f'Creating test repo at: {constants.installed_repo_dir}')

    with open(common.configuration.agent_config.aws_creds_fp, 'w') as f:
        f.write('')

    with open(common.configuration.agent_config.agent_registration_fp, 'w') as f:
        f.write(
            json.dumps(
                {
                    'agent_id': test_constants.test_agent_id,
                    'operations_queue_url': test_constants.test_operations_queue_url,
                    'version': test_constants.test_version,
                    'agent_key': test_constants.test_agent_key,  # TODO: This is not used in the agent
                    'ip_address': test_constants.test_ip_address  # TODO: This is not used in the agent
                }
            )
        )
        f.write('\n')


