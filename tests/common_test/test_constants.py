from datetime import datetime

from cumulonimbus_models.operations import Operation, OperationResultStatus, OperationType

from agent.models import AgentOperation, AgentState, VersionInfo


test_agent_id = 'test-agent-id'
test_operations_queue_url = 'https://sqs.us-west-1.amazonaws.com/012345678901/test'
test_agent_key = 'test-agent-key'
test_ip_address = '000.000.000.000'
test_major_version = 0
test_minor_version = 0
test_patch_version = 0
test_rc_version = 9
test_version_info = VersionInfo(
    major=test_major_version,
    minor=test_minor_version,
    patch=test_patch_version,
    release_candidate=test_rc_version
)
test_version = str(test_version_info)
test_op = Operation(
    id='test-operation-id',
    type=OperationType.UPDATE,
    parameters={},
)

test_op_started = datetime.now()
test_agent_op = AgentOperation(
    started=test_op_started,
    operation=test_op,
    status=OperationResultStatus.PENDING
)

test_agent_state = AgentState(
    agent_id=test_agent_id,
    queue_url=test_operations_queue_url,
    version=test_version
)