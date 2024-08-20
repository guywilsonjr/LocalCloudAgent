import os
import shutil

import pytest

from common_test import eval_constants


@pytest.mark.asyncio
async def test_check_systemd_service() -> None:
    from local_cloud_agent.common.configuration import agent_config
    from local_cloud_agent.common import constants
    from local_cloud_agent.agent.operations import update
    resp = await update.check_systemd_service()
    assert resp is True
    with open(agent_config.installed_service_fp, 'w') as f:
        f.write(constants.service_file_data)
    resp = await update.check_systemd_service()
    assert resp is False


@pytest.mark.asyncio
async def test_reload(mocker):
    from local_cloud_agent.agent.operations import update
    mocker.patch('asyncio.subprocess.create_subprocess_shell')
    await update.reload(eval_constants.test_agent_op)


@pytest.mark.asyncio
async def test_update():
    from local_cloud_agent.agent.operations import update
    from local_cloud_agent.common.configuration import agent_config
    os.makedirs(agent_config.operations_dir, exist_ok=True)
    with pytest.raises(SystemExit):
        await update.update_local_cloud_agent(eval_constants.test_agent_op)
    shutil.rmtree(agent_config.operations_dir)
