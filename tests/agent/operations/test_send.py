from datetime import datetime

import pytest
from cumulonimbus_models.operations import Operation, OperationResult, OperationResultStatus, OperationType

from agent.models import AgentState, PersistedOperation
from tests.test_common.test_fixtures import setup_file_system


class MockResponse:

    def __init__(self):
        self.status = 200

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


test_op = Operation(
    id='test-operation-id',
    type=OperationType.UPDATE,
    parameters={},
)


@pytest.mark.asyncio
async def test_send_operation_result(setup_file_system, mocker):
    test_persist_op = PersistedOperation(
        started=datetime.now(),
        operation=test_op,
        status=OperationResultStatus.PENDING
    )
    test_output = OperationResult(operation_output='SUCCESS', operation_status=OperationResultStatus.SUCCESS)

    resp = MockResponse()
    a = mocker.patch('aiohttp.ClientSession.patch', return_value=resp)
    from agent.operations import send
    test_agent_state = AgentState(agent_id='test-agent-id', queue_url='test-queue-url', version='test-version')
    await send.send_operation_result(test_agent_state, test_persist_op, test_output)
    a.assert_called_once()