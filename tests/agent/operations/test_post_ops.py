from datetime import datetime

import pytest
from cumulonimbus_models.operations import OperationResult, OperationResultStatus

from local_cloud_agent.agent.models import AgentState, AgentOperation
from common_test import test_constants, test_mocks


@pytest.mark.usefixtures("root_fakefs", "fake_base_fs", "installed", "registered_agent")
@pytest.mark.asyncio
async def test_complete_operation(mocker):
    test_persist_op = AgentOperation(
        started=datetime.now(),
        operation=test_constants.test_op,
        status=OperationResultStatus.PENDING
    )
    test_output = OperationResult(operation_output='SUCCESS', operation_status=OperationResultStatus.SUCCESS)
    test_agent_state = AgentState(agent_id='test-agent-id', queue_url='test-queue-url', version='test-version')
    resp = test_mocks.MockAIOHttpResponse()
    a = mocker.patch('aiohttp.ClientSession.patch', return_value=resp)
    from local_cloud_agent.agent.operations import send
    await send.send_operation_result(test_agent_state, test_persist_op, test_output)
    a.assert_called_once()
