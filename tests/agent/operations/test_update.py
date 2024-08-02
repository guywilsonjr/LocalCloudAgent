import pytest
from tests.common_test import test_constants


@pytest.mark.usefixtures("installed_repo_dir", "root_fakefs", "fake_base_fs", "installed", "registered_agent")
@pytest.mark.asyncio
async def test_check_systemd_service(monkeypatch):
    # TODO
    pass

