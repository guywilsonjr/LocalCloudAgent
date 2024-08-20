import pytest
import os

import pytest_mock

from tests.common_test import eval_constants


@pytest.mark.usefixtures("registered_agent")
@pytest.mark.asyncio
async def test_0startup() -> None:
    from local_cloud_agent.agent import initialize
    await initialize.startup(eval_constants.test_agent_state)
    '''test update_local_cloud_agent
    from local_cloud_agent.agent.operations.update import update_local_cloud_agent

    with pytest.raises(SystemExit):
        await update_local_cloud_agent(eval_constants.test_agent_op)
    await initialize.startup(eval_constants.test_agent_state)
    '''


@pytest.mark.usefixtures("registered_agent")
@pytest.mark.asyncio
async def test_1check_for_updates(mocker: pytest_mock.plugin.MockerFixture) -> None:
    from local_cloud_agent.common.configuration import agent_config

    from local_cloud_agent.agent.initialize import check_for_updates
    await check_for_updates(eval_constants.test_agent_state)
    with open(agent_config.update_operation_fp, 'w') as f:
        f.write(eval_constants.test_agent_op.model_dump_json())

    mocker.patch('aiohttp.ClientSession.patch')
    await check_for_updates(eval_constants.test_agent_state)
    os.remove(agent_config.update_operation_fp)




