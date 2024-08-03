import os
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

from pyfakefs.fake_filesystem_unittest import Patcher

from common_test import test_constants


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

#aiofile.async_open = asynccontextmanager(mock_async_open)


@pytest.fixture(scope='function')
def root_fakefs():
    logging.info('root_fakefs')
    with Patcher(allow_root_user=True) as patcher:
        yield patcher.fs



@pytest.fixture(scope='function')
def fake_base_fs():
    logging.info('fake_base_fs')
    import os
    from common import constants
    from local_cloud_agent.common.common_logger import agent_config
    assert not os.path.exists(agent_config.etc_dir)

    base_dirs = [
        '/usr/lib/ssl/certs',
        agent_config.etc_dir,
        agent_config.var_log_dir,
        agent_config.var_local_dir,
        agent_config.home_dir,
        agent_config.conf_dir
    ]
    [os.makedirs(base_dir) for base_dir in base_dirs]
    os.makedirs('/usr/bin')
    with open('/usr/bin/python3.12', 'w') as file:
        file.write('')
    yield
    shutil.rmtree('/usr/local')
    shutil.rmtree('/etc')
    shutil.rmtree('/var')
    shutil.rmtree(agent_config.home_dir)
    shutil.rmtree('/usr/lib/ssl/certs')



@pytest.fixture(scope='function')
def aws():
    logging.info('aws')
    import os
    from local_cloud_agent.common.common_logger import agent_config
    os.makedirs(agent_config.aws_dir)
    with open(agent_config.aws_creds_fp, 'w') as f:
        f.write('')
    yield


@pytest.fixture(scope='function')
def installed(aws: None):
    logging.info('installed')
    import os
    from common import constants
    from local_cloud_agent.common.common_logger import agent_config
    os.makedirs(agent_config.agent_dir)
    os.makedirs(agent_config.operations_dir)

    with open(agent_config.installed_service_fp, 'w') as file:
        file.write(constants.service_file_data)

    yield
    shutil.rmtree(agent_config.metadata_dir)
    os.remove(constants.installed_service_conf_fp)
    shutil.rmtree(agent_config.aws_dir)


@pytest.fixture(scope='function')
def registered_agent():
    import os
    from local_cloud_agent.common.common_logger import agent_config
    with open(agent_config.agent_registration_fp, 'w') as f:
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

    logging.info(f'Registered agent {agent_config.agent_registration_fp}')
    yield
    os.remove(agent_config.agent_registration_fp)
