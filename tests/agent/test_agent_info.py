import pytest
from cumulonimbus_models.agent import AgentRegisterResponse
from tests.test_common.test_fixtures import setup_file_system


@pytest.mark.asyncio
async def test_get_registration(setup_file_system):
    from local_cloud_agent.agent import agent_info
    resp = await agent_info.get_registration()
    assert resp == AgentRegisterResponse(
        agent_id='test-agent-id',
        agent_key='test-agent-key',
        ip_address='000.000.000.000',
        operations_queue_url='https://sqs.us-west-1.amazonaws.com/012345678901/test'
    )


@pytest.mark.asyncio
async def test_startup(setup_file_system):
    from local_cloud_agent.agent import agent_info
    await agent_info.startup()

