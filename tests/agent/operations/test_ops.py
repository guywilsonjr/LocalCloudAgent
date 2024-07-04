import pytest


@pytest.mark.usefixtures("root_fakefs", "fake_base_fs", "installed", "registered_agent")
def test_ops():
    from agent.operations import ops
    assert ops
