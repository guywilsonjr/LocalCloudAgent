from datetime import datetime

import pytest
from cumulonimbus_models.operations import OperationResult, OperationResultStatus
from types_aiobotocore_sqs.type_defs import MessageTypeDef

from local_cloud_agent.agent.models import AgentState, AgentOperation
from local_cloud_agent.agent.operations.util import send_operation_result
from tests.common_test import eval_constants, mocks


@pytest.mark.usefixtures("registered_agent")
@pytest.mark.asyncio
async def test_init_operation():
    from local_cloud_agent.common.configuration import agent_config
    start_dt = datetime.now()

    test_persist_op = AgentOperation(
        started=datetime.now(),
        operation=eval_constants.test_op,
        status=OperationResultStatus.PENDING
    )
    with open(agent_config.operation_log_fp, 'w') as f:
        f.write(test_persist_op.model_dump_json() + '\n')
    from local_cloud_agent.agent.operations import util
    test_msg = MessageTypeDef(
        MessageId='test-message-id',
        Body=eval_constants.test_op.model_dump_json()
    )
    await util.init_operation(test_msg)
    with open(agent_config.operation_log_fp, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 2
    persisted_op = AgentOperation.model_validate_json(lines[0].strip())
    assert OperationResultStatus.PENDING == persisted_op.status
    assert eval_constants.test_op == persisted_op.operation
    assert start_dt < persisted_op.started


@pytest.mark.usefixtures("registered_agent")
@pytest.mark.asyncio
async def test_send_operation_result(mocker):
    test_persist_op = AgentOperation(
        started=datetime.now(),
        operation=eval_constants.test_op,
        status=OperationResultStatus.PENDING
    )
    test_output = OperationResult(operation_output='SUCCESS', operation_status=OperationResultStatus.SUCCESS)

    resp = mocks.MockAIOHttpResponse()
    a = mocker.patch('aiohttp.ClientSession.patch', return_value=resp)
    test_agent_state = AgentState(agent_id='test-agent-id', queue_url='test-queue-url', version='test-version')
    await send_operation_result(test_agent_state, test_persist_op, test_output)
    a.assert_called_once()


@pytest.mark.usefixtures("registered_agent")
@pytest.mark.asyncio
async def test_complete_operation(mocker):
    test_persist_op = AgentOperation(
        started=datetime.now(),
        operation=eval_constants.test_op,
        status=OperationResultStatus.PENDING
    )
    test_output = OperationResult(operation_output='SUCCESS', operation_status=OperationResultStatus.SUCCESS)
    test_agent_state = AgentState(agent_id='test-agent-id', queue_url='test-queue-url', version='test-version')
    resp = mocks.MockAIOHttpResponse()
    a = mocker.patch('aiohttp.ClientSession.patch', return_value=resp)
    await send_operation_result(test_agent_state, test_persist_op, test_output)
    a.assert_called_once()
