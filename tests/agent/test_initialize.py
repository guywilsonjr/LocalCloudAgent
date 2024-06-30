import os
import shutil

import pytest

from common.configuration import agent_config
from tests.test_common.test_fixtures import setup_file_system



@pytest.mark.asyncio
async def test_check_for_updates(setup_file_system):
    from agent.initialize import check_for_updates
    await check_for_updates()


@pytest.mark.asyncio
async def test_startup(setup_file_system):
    from agent import initialize
    await initialize.startup()


def test_ensure_dirs_exist():
    from agent.initialize import ensure_dirs_exist
    ensure_dirs_exist()
    assert os.path.exists(agent_config.metadata_dir)
    assert os.path.exists(agent_config.agent_dir)
    assert os.path.exists(agent_config.operations_dir)


def test_validate_fs():
    from agent.initialize import validate_fs
    validate_fs()
