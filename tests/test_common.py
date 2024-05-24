import json
import os

import pytest_asyncio
import constants


def rmfile(path):
    if os.path.exists(path):
        os.remove(path)

def rmdir(path):
    if os.path.exists(path):
        os.rmdir(path)


@pytest_asyncio.fixture(scope='session')
def setup_home_dir():
    os.makedirs(constants.home_dir, exist_ok=True)
    os.makedirs(constants.repo_dir, exist_ok=True)

    os.makedirs(constants.aws_dir, exist_ok=True)
    with open(constants.aws_creds_fp, 'w') as f:
        f.write('')

    os.makedirs(constants.local_cloud_agent_dir, exist_ok=True)
    with open(constants.latest_running_version_fp, 'w') as f:
        f.write('a.b.c')

    os.makedirs(constants.operations_dir, exist_ok=True)
    os.makedirs(constants.agent_dir, exist_ok=True)
    with open(constants.agent_registration_fp, 'w') as f:
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
    rmdir(f'{constants.home_dir}/.cache')

    rmfile(constants.agent_registration_fp)
    rmdir(constants.operations_dir)
    rmdir(constants.agent_dir)
    rmfile(constants.latest_running_version_fp)
    rmdir(constants.local_cloud_agent_dir)
    rmfile(constants.aws_creds_fp)
    rmdir(constants.aws_dir)
    rmdir(constants.repo_dir)
    rmdir(f'{constants.home_dir}/repos')
    rmdir(constants.home_dir)




