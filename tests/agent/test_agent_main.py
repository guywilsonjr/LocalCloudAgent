import pytest


@pytest.mark.usefixtures("registered_agent")
def test_main():
    from local_cloud_agent.agent import main
    # TODO use mocker
    assert main