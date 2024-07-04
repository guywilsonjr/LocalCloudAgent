import pytest
from pyfakefs.fake_filesystem import FakeFilesystem


@pytest.mark.usefixtures("root_fakefs", "fake_base_fs", "installed", "registered_agent")
@pytest.mark.asyncio
async def test_check_for_updates():
    from agent.initialize import check_for_updates
    await check_for_updates()


@pytest.mark.usefixtures("root_fakefs", "fake_base_fs", "installed", "registered_agent")
@pytest.mark.asyncio
async def test_startup():
    from agent import initialize
    await initialize.startup()

