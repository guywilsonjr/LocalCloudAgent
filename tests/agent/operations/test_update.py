import pytest


@pytest.mark.asyncio
async def test_check_systemd_service():
    from agent.operations.update import check_systemd_service
    await check_systemd_service()


