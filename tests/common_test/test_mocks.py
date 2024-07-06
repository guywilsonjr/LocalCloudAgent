import logging
import os

from common import constants
from tests.common_test import test_constants


class MockCommit:
    committed_datetime = 0



class MockTagRef:
    commit = MockCommit()
    name = test_constants.test_version


class MockGit:
    def __init__(self, *args, **kwargs):
        pass

    def ls_remote(self, *args, **kwargs):
        return test_constants.test_version


class MockGitRepo:
    tags = [MockTagRef()]
    def __init__(self, *args, **kwargs):
        logging.info('creating repo')
        pass

    @staticmethod
    def clone_from(*args, **kwargs):
        logging.info('Cloning from')
        os.makedirs(constants.repo_python_path)


class MockAIOHttpResponse:

    def __init__(self):
        self.status = 200

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self
