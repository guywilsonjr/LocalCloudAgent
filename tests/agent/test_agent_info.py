import pytest
from cumulonimbus_models.agent import AgentRegisterResponse

from agent.models import AgentState
from tests.common_test import test_constants
from tests.common_test.test_fixtures import setup_file_system


@pytest.mark.asyncio
async def test_get_registration():
    from agent import agent_info
    resp = await agent_info.get_registration()
    assert resp == AgentRegisterResponse(
        agent_id=test_constants.test_agent_id,
        agent_key=test_constants.test_agent_key,
        ip_address=test_constants.test_ip_address,
        operations_queue_url=test_constants.test_operations_queue_url
    )


@pytest.mark.asyncio
async def test_get_agent_state(setup_file_system):
    from agent import agent_info
    expected_agent_state = AgentState(
        agent_id=test_constants.test_agent_id,
        queue_url=test_constants.test_operations_queue_url,
        version=test_constants.test_version
    )
    agent_state = await agent_info.get_agent_state()
    assert expected_agent_state == agent_state
