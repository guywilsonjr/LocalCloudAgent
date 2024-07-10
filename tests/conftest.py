import json
import logging
import os
import shutil
import subprocess
from typing import Generator

import pytest
import aiofile

from contextlib import asynccontextmanager

from pyfakefs.fake_filesystem_unittest import Patcher

from tests.common_test import test_constants


class BaseMock:
    def __init__(self, *args, **kwargs):
        pass



@asynccontextmanager
async def mock_async_open(fp: str, mode: str) -> Generator[BaseMock, None, None]:
    class MockFileObj(BaseMock):
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


def mock_venv_create(*args, **kwargs):
    import os
    from common.configuration import agent_config
    logging.info('Making mock venv')
    os.makedirs(agent_config.venv_dir)


# Maybe use mocker for the git stuff
import venv


venv.create = mock_venv_create


class SubprocessRunResult:
    stdout: str = ''



def mock_subprocess_run(*args, **kwargs):
    logging.info('Mock Subprocess Running')
    return SubprocessRunResult()


subprocess.run = mock_subprocess_run

aiofile.async_open = mock_async_open


@pytest.fixture(scope='function')
def root_fakefs():
    logging.info('root_fakefs')
    with Patcher(allow_root_user=True) as patcher:
        yield patcher.fs


@pytest.fixture(scope='function')
def usr_local_src(monkeypatch, tmp_path):
    logging.info('usr_local_src')
    with monkeypatch.context() as m:
        from common import constants
        m.setenv(constants.repo_prefix_env_var, str(tmp_path))
        os.makedirs(f'{tmp_path}/usr/local/src')
        yield


@pytest.fixture(scope='function')
def installed_repo_dir(monkeypatch, tmp_path):
    logging.info('installed_repo_dir')
    with monkeypatch.context() as m:
        m.setenv('LOCAL_CLOUD_AGENT_REPO_PREFIX', str(tmp_path))
        from common import git_common
        git_common.clone_repo()
        yield


@pytest.fixture(scope='function')
def fake_base_fs():
    logging.info('fake_base_fs')
    import os
    from common import constants
    assert not os.path.exists(constants.parent_conf_dir)

    base_dirs = [
        '/usr/lib/ssl/certs',
        constants.parent_conf_dir,
        constants.parent_log_dir,
        constants.parent_metadata_dir,
        constants.root_home_dir,
        constants.system_usr_local_dir,
        constants.installed_service_conf_dir
    ]
    [os.makedirs(base_dir) for base_dir in base_dirs]
    os.makedirs('/usr/bin')
    with open('/usr/bin/python3.12', 'w') as file:
        file.write('')
    yield
    shutil.rmtree('/usr/local')
    shutil.rmtree('/etc')
    shutil.rmtree('/var')
    shutil.rmtree('/root')
    shutil.rmtree('/usr/lib/ssl/certs')



@pytest.fixture(scope='function')
def aws():
    logging.info('aws')
    import os
    from common.configuration import agent_config
    os.makedirs(agent_config.aws_dir)
    with open(agent_config.aws_creds_fp, 'w') as f:
        f.write('')
    yield


@pytest.fixture(scope='function')
def installed(aws: None):
    logging.info('installed')
    import os
    from common import constants
    from common.configuration import agent_config
    os.makedirs(agent_config.agent_dir)
    os.makedirs(agent_config.operations_dir)
    os.makedirs(constants.install_log_dir)
    os.makedirs(f'{constants.installed_service_conf_dir}/{constants.lower_keyword}')

    with open(agent_config.installed_service_fp, 'w') as file:
        file.write(constants.service_file_data)

    yield
    shutil.rmtree(f'{constants.installed_service_conf_dir}/{constants.lower_keyword}')
    shutil.rmtree(constants.install_log_dir)
    shutil.rmtree(agent_config.metadata_dir)
    os.remove(constants.installed_service_conf_fp)
    shutil.rmtree(constants.aws_dir)


@pytest.fixture(scope='function')
def registered_agent():
    import os
    from common.configuration import agent_config
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
