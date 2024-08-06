import pytest
from tests.common_test import eval_constants


@pytest.mark.asyncio
async def test_check_systemd_service():
    from local_cloud_agent.agent.operations import update

