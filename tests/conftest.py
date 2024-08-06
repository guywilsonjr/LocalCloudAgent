import os

from local_cloud_agent.common import constants


if 'INDOCKER' not in os.environ:
    raise Exception('INDOCKER not in os.environ')

if os.environ.get('INDOCKER') != '1':
    raise Exception('INDOCKER not set to 1')
import json
import logging

import shutil
from typing import Any, Generator

import pytest
import aiofile

from contextlib import asynccontextmanager
from tests.common_test import eval_constants


@asynccontextmanager
async def mock_async_open(fp: str, mode: str) -> Generator[Any, None, None]:
    class MockFileObj:
        def __init__(self):
            logging.info('Opening file %s', fp)
            self.fh = open(fp, mode)

        async def write(self, data: str) -> None:
            self.fh.write(data)

        async def read(self) -> str:
            return self.fh.read()

    f = None
    try:
        f = MockFileObj()
        yield f
    finally:
        if f:
            f.fh.close()

aiofile.async_open = mock_async_open


@pytest.fixture(scope='function')
def installed():
    from local_cloud_agent.common.configuration import agent_config
    os.makedirs(agent_config.aws_dir, exist_ok=True)
    os.makedirs(agent_config.metadata_dir, exist_ok=True)
    os.makedirs(agent_config.agent_dir, exist_ok=True)
    os.makedirs(agent_config.operations_dir, exist_ok=True)
    os.makedirs(agent_config.conf_dir, exist_ok=True)
    os.makedirs(agent_config.log_dir, exist_ok=True)
    yield
    shutil.rmtree(agent_config.agent_dir)
    shutil.rmtree(agent_config.operations_dir)
    shutil.rmtree(agent_config.metadata_dir)
    shutil.rmtree(agent_config.conf_dir)
    shutil.rmtree(agent_config.log_dir)
    shutil.rmtree(agent_config.aws_dir)


@pytest.fixture(scope='function')
def registered_agent(installed):
    import os
    from local_cloud_agent.common.configuration import agent_config
    with open(agent_config.agent_registration_fp, 'w') as f:
        f.write(
            json.dumps(
                {
                    'agent_id': eval_constants.test_agent_id,
                    'operations_queue_url': eval_constants.test_operations_queue_url,
                    'version': eval_constants.test_version,
                    'agent_key': eval_constants.test_agent_key,  # TODO: This is not used in the agent
                    'ip_address': eval_constants.test_ip_address  # TODO: This is not used in the agent
                }
            )
        )
        f.write('\n')

    logging.info(f'Registered agent {agent_config.agent_registration_fp}')
    yield
    os.remove(agent_config.agent_registration_fp)
