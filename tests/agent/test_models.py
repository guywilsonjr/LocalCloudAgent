from datetime import datetime

from cumulonimbus_models.operations import Operation, OperationResultStatus, OperationType


def test_models():
    from local_cloud_agent.agent import models
    assert models.AgentState(
        agent_id='test-agent-id',
        queue_url='test-queue-url',
        version='test-version'
    )
    assert models.AgentOperation(
        started=datetime.now(),
        operation=Operation(id='test-operation-id', type=OperationType.UPDATE, parameters={}),
        status=OperationResultStatus.SUCCESS
    )
