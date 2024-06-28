from datetime import datetime

from cumulonimbus_models.operations import Operation, OperationResultStatus, OperationType


def test_models():
    from agent import models
    assert models.AgentState(
        agent_id='test-agent-id',
        queue_url='test-queue-url',
        version='test-version'
    )
    assert models.PersistedOperation(
        started=datetime.now(),
        operation=Operation(id='test-operation-id', type=OperationType.UPDATE, parameters={}),
        status=OperationResultStatus.SUCCESS
    )
