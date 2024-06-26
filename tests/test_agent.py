import pytest
from cumulonimbus_models.agent import AgentRegisterResponse
from test_common import setup_file_system


@pytest.mark.asyncio
async def test_get_registration(setup_file_system):
    import agent
    resp = await agent.get_registration()
    assert resp == AgentRegisterResponse(
        agent_id='test-agent-id',
        agent_key='test-agent-key',
        ip_address='000.000.000.000',
        operations_queue_url='https://sqs.us-west-1.amazonaws.com/012345678901/test'
    )
