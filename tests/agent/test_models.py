from datetime import datetime

from cumulonimbus_models.operations import Operation, OperationResultStatus, OperationType

from local_cloud_agent.agent.models import VersionInfo


def test_models() -> None:
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
    str(VersionInfo(major=0, minor=0, patch=0, release_candidate=None))
