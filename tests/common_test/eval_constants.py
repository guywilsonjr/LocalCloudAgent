from datetime import datetime

from cumulonimbus_models.agent import AgentRegisterRequest, AgentRegisterResponse
from cumulonimbus_models.operations import Operation, OperationResult, OperationResultStatus, OperationType

from local_cloud_agent.agent.models import AgentOperation, AgentOperationResult, AgentState, VersionInfo


test_agent_id = 'test-agent-id'
test_operations_queue_url = 'https://sqs.us-west-1.amazonaws.com/012345678901/test'
test_agent_key = 'test-agent-key'
test_ip_address = '000.000.000.000'
test_major_version = 0
test_minor_version = 0
test_patch_version = 0
test_rc_version = 10
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

test_shell_op = Operation(
    id='test-operation-id',
    type=OperationType.SHELL_COMMAND,
    parameters={'cmd': 'ls'}
)

test_op_started = datetime.now()
test_agent_op = AgentOperation(
    started=test_op_started,
    operation=test_op,
    status=OperationResultStatus.PENDING
)

test_agent_shell_op = AgentOperation(
    started=test_op_started,
    operation=test_shell_op,
    status=OperationResultStatus.PENDING
)

test_agent_state = AgentState(
    agent_id=test_agent_id,
    queue_url=test_operations_queue_url,
    version=test_version
)
test_register_agent_response = AgentRegisterResponse(agent_id=test_agent_id, agent_key=test_agent_key, ip_address=test_ip_address, operations_queue_url=test_operations_queue_url)
test_register_agent_request = AgentRegisterRequest(hostname='test-hostname')


async def test_op_with_post_op(*args, **kwargs) -> AgentOperationResult:
    return AgentOperationResult(
        operation_result=OperationResult(operation_output='', operation_status=OperationResultStatus.PENDING),
        post_op=test_async_get_none
    )

async def test_async_exception(*args, **kwargs) -> None:
    raise Exception()


async def test_async_get_none(*args, **kwargs) -> None:
    return None




test_agent_operation_result = AgentOperationResult(
    operation_result=OperationResult(operation_output='', operation_status=OperationResultStatus.PENDING),
    post_op=test_async_get_none
)


async def test_op_func(op: AgentOperation) -> AgentOperationResult:
    assert op
    return test_agent_operation_result