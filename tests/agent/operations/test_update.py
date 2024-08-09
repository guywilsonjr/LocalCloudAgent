import pytest

from local_cloud_agent.common.configuration import agent_config
from tests.common_test import eval_constants


@pytest.mark.asyncio
async def test_check_systemd_service():
    from local_cloud_agent.agent.operations import update
    resp = await update.check_systemd_service()
    assert resp is True
    with open(agent_config.installed_service_fp, 'w') as f:
        f.write(' ')
    resp = await update.check_systemd_service()
    assert resp is True

