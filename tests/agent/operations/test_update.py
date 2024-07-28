import pytest
from tests.common_test import test_constants


@pytest.mark.usefixtures("installed_repo_dir", "root_fakefs", "fake_base_fs", "installed", "registered_agent")
@pytest.mark.asyncio
async def test_check_systemd_service(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr('common.systemd.reload_systemd', lambda: None)
        from agent.operations.update import check_systemd_service, update_local_cloud_agent
        await check_systemd_service()
        await update_local_cloud_agent(test_constants.test_agent_op)


