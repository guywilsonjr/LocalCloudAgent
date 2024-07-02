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
        pass


class MockAIOHttpResponse:

    def __init__(self):
        self.status = 200

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self
