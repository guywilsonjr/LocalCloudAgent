from typing import Generator

import pyfakefs.fake_filesystem
import pytest
import aiofile

from contextlib import asynccontextmanager

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
from tests.common_test import test_mocks
import git
git.Git = test_mocks.MockGit
git.Repo = test_mocks.MockGitRepo
git.TagReference = test_mocks.MockTagRef


@pytest.fixture(scope='function', autouse=True)
def fake_filesystem(fs_session: pyfakefs.fake_filesystem.FakeFilesystem):  # pylint:disable=invalid-name
    """Variable name 'fs' causes a pylint warning. Provide a longer name
    acceptable to pylint for use in tests.
    """
    aiofile.async_open = mock_async_open
    yield fs_session
