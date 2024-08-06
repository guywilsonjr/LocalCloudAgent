import pytest
from cumulonimbus_models.agent import AgentRegisterResponse

from local_cloud_agent.agent.models import AgentState
from tests.common_test import eval_constants


@pytest.mark.usefixtures("registered_agent")
@pytest.mark.asyncio
async def test_register_agent_request():
    from local_cloud_agent.agent import agent_info
    resp = await agent_info.get_registration()
    assert resp == AgentRegisterResponse(
        agent_id=eval_constants.test_agent_id,
        agent_key=eval_constants.test_agent_key,
        ip_address=eval_constants.test_ip_address,
        operations_queue_url=eval_constants.test_operations_queue_url
    )


@pytest.mark.usefixtures("registered_agent")
@pytest.mark.asyncio
async def test_get_registration():
    from local_cloud_agent.agent import agent_info
    resp = await agent_info.get_registration()
    assert resp == AgentRegisterResponse(
        agent_id=eval_constants.test_agent_id,
        agent_key=eval_constants.test_agent_key,
        ip_address=eval_constants.test_ip_address,
        operations_queue_url=eval_constants.test_operations_queue_url
    )



@pytest.mark.usefixtures("registered_agent")
@pytest.mark.asyncio
async def test_get_agent_state():
    from local_cloud_agent.agent import agent_info
    expected_agent_state = AgentState(
        agent_id=eval_constants.test_agent_id,
        queue_url=eval_constants.test_operations_queue_url,
        version='TODO'
    )
    agent_state = await agent_info.get_agent_state()
    assert expected_agent_state == agent_state
