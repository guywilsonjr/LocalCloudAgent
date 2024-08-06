import pytest

from tests.common_test import eval_constants


@pytest.mark.usefixtures("registered_agent")
@pytest.mark.asyncio
async def test_0startup():
    from local_cloud_agent.agent import initialize
    await initialize.startup(eval_constants.test_agent_state)


@pytest.mark.usefixtures("registered_agent")
@pytest.mark.asyncio
async def test_1check_for_updates():
    from local_cloud_agent.agent.initialize import check_for_updates
    await check_for_updates(eval_constants.test_agent_state)



