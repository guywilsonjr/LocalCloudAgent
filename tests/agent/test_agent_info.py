import logging

import pytest
from cumulonimbus_models.agent import AgentRegisterResponse

from agent.models import AgentState
from tests.common_test import test_constants


@pytest.mark.usefixtures("root_fakefs", "fake_base_fs", "installed", "registered_agent")
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



@pytest.mark.usefixtures("root_fakefs", "fake_base_fs", "installed", "registered_agent")
@pytest.mark.asyncio
async def test_get_agent_state():
    import os
    from agent import agent_info
    expected_agent_state = AgentState(
        agent_id=test_constants.test_agent_id,
        queue_url=test_constants.test_operations_queue_url,
        version=test_constants.test_version
    )
    agent_state = await agent_info.get_agent_state()
    assert expected_agent_state == agent_state
