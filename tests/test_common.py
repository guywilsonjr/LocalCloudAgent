import json
import os
import shutil

import pytest_asyncio
from configuration import agent_config


def rmfile(path):
    if os.path.exists(path):
        os.remove(path)


def rmdir(path):
    if os.path.exists(path):
        os.rmdir(path)


def rmtree(path):
    if os.path.exists(path):
        shutil.rmtree(path)


@pytest_asyncio.fixture(scope='session')
def setup_file_system():
    os.makedirs(agent_config.log_dir, exist_ok=True)
    os.makedirs(agent_config.home_dir, exist_ok=True)
    os.makedirs(agent_config.repo_dir, exist_ok=True)

    os.makedirs(agent_config.aws_dir, exist_ok=True)
    with open(agent_config.aws_creds_fp, 'w') as f:
        f.write('')

    os.makedirs(agent_config.local_cloud_agent_dir, exist_ok=True)
    os.makedirs(agent_config.operations_dir, exist_ok=True)
    os.makedirs(agent_config.agent_dir, exist_ok=True)
    with open(agent_config.agent_registration_fp, 'w') as f:
        f.write(
            json.dumps(
                {
                    "agent_id": "test-agent-id",
                    "agent_key": "test-agent-key",
                    "ip_address": "000.000.000.000",
                    "operations_queue_url": "https://sqs.us-west-1.amazonaws.com/012345678901/test"
                }
            )
        )
        f.write('\n')

    yield None
    rmtree('tests/.testfs')





