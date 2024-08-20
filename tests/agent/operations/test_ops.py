import pytest


@pytest.mark.usefixtures("registered_agent")
def test_ops() -> None:
    from local_cloud_agent.agent.operations import ops
    assert ops
