from importlib.metadata import PackageNotFoundError

import pytest_mock

from common_test import eval_constants


def test___init__() -> None:
    import local_cloud_agent
    assert local_cloud_agent.get_version() == eval_constants.test_version



def test_fail___init__(mocker: pytest_mock.plugin.MockerFixture) -> None:
    mocker.patch('importlib.metadata.version', side_effect=PackageNotFoundError())
    import local_cloud_agent
    assert local_cloud_agent.get_version() == 'Unknown'


