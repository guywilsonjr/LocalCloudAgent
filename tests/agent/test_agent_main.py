import pytest


@pytest.mark.usefixtures("root_fakefs", "fake_base_fs", "installed", "registered_agent")
def test_main():
    from agent import main
    # TODO use mocker
    assert main