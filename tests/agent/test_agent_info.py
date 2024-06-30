import pytest
from cumulonimbus_models.agent import AgentRegisterResponse

from agent.models import AgentState
from tests.test_common.test_fixtures import test_agent_id, test_operations_queue_url, test_version, setup_file_system


@pytest.mark.asyncio
async def test_get_registration():
    from agent import agent_info
    resp = await agent_info.get_registration()
    assert resp == AgentRegisterResponse(
        agent_id='test-agent-id',
        agent_key='test-agent-key',
        ip_address='000.000.000.000',
        operations_queue_url='https://sqs.us-west-1.amazonaws.com/012345678901/test'
    )


@pytest.mark.asyncio
async def test_get_agent_state(setup_file_system):
    from agent import agent_info
    expected_agent_state = AgentState(
        agent_id=test_agent_id,
        queue_url=test_operations_queue_url,
        version=test_version
    )
    agent_state = await agent_info.get_agent_state()
    assert expected_agent_state == agent_state
