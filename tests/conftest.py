import json
import os
import shutil
from typing import Generator

import pyfakefs.fake_filesystem
import pytest
import aiofile

from contextlib import asynccontextmanager

from pyfakefs.fake_filesystem_unittest import Patcher
import common.configuration
from common.configuration import agent_config

from common import constants
from tests.common_test import test_constants


class BaseMock:
    def __init__(self, *args, **kwargs):
        pass


@asynccontextmanager
async def mock_async_open(fp: str, mode: str) -> Generator[BaseMock, None, None]:
    class MockFileObj(BaseMock):
        def __init__(self):
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


# Maybe use mocker for the git stuff
from tests.common_test import test_mocks
import git
git.Git = test_mocks.MockGit
git.Repo = test_mocks.MockGitRepo
git.TagReference = test_mocks.MockTagRef


@pytest.fixture(autouse=True)
def fake_filesystem(fs_session: pyfakefs.fake_filesystem.FakeFilesystem):  # pylint:disable=invalid-name
    """Variable name 'fs' causes a pylint warning. Provide a longer name
    acceptable to pylint for use in tests.
    """
    aiofile.async_open = mock_async_open
    yield fs_session


@pytest.fixture
def root_fakefs():
    with Patcher(allow_root_user=True) as patcher:
        yield patcher.fs


@pytest.fixture
def fake_base_fs():
    base_dirs = [
        constants.parent_conf_dir,
        constants.parent_log_dir,
        constants.parent_metadata_dir,
        constants.root_dir,
        constants.system_usr_local_dir,
        constants.installed_service_conf_dir
    ]
    [os.makedirs(base_dir) for base_dir in base_dirs]
    yield
    [shutil.rmtree(base_dir) for base_dir in reversed(base_dirs)]


@pytest.fixture
def aws():
    os.makedirs(agent_config.aws_dir)
    with open(agent_config.aws_creds_fp, 'w') as f:
        f.write('')
    yield


@pytest.fixture
def installed(aws: None):
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
    shutil.rmtree(common.constants.aws_dir)


@pytest.fixture
def registered_agent():
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

    print(f'Registered agent {agent_config.agent_registration_fp}')
    yield
    os.remove(agent_config.agent_registration_fp)
