import pytest
from test_common import setup_home_dir

@pytest.mark.asyncio
async def test_versions(setup_home_dir):
    import updater
    last_version = await updater.fetch_prev_run_version()
    assert last_version == 'a.b.c'
    await updater.save_latest_running_version()
    new_version = await updater.fetch_prev_run_version()
    assert new_version == 'x.y.z'

