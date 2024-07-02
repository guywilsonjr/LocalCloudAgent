import pytest

from tests.common_test.test_fixtures import setup_file_system



@pytest.mark.asyncio
async def test_check_for_updates(setup_file_system):
    from agent.initialize import check_for_updates
    await check_for_updates()


@pytest.mark.asyncio
async def test_startup(setup_file_system):
    from agent import initialize
    await initialize.startup()

