from datetime import datetime

import pytest
from types_aiobotocore_sqs.type_defs import MessageTypeDef
from cumulonimbus_models.operations import Operation, OperationResult, OperationResultStatus, OperationType

from agent.models import AgentState, PersistedOperation
from agent.configuration import agent_config
from tests.test_common.test_fixtures import setup_file_system, rmfile


test_op = Operation(
    id='test-operation-id',
    type=OperationType.UPDATE,
    parameters={},
)


@pytest.mark.asyncio
async def test_init_operation(setup_file_system):
    start_dt = datetime.now()

    test_persist_op = PersistedOperation(
        started=datetime.now(),
        operation=test_op,
        status=OperationResultStatus.PENDING
    )
    with open(agent_config.operation_log_fp, 'w') as f:
        f.write(test_persist_op.model_dump_json() + '\n')
    from agent.operations import util
    test_msg = MessageTypeDef(
        MessageId='test-message-id',
        Body=test_op.model_dump_json()
    )
    await util.init_operation(test_msg)
    with open(agent_config.operation_log_fp, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 2
    persisted_op = PersistedOperation.model_validate_json(lines[0].strip())
    assert OperationResultStatus.PENDING == persisted_op.status
    assert test_op == persisted_op.operation
    assert start_dt < persisted_op.started
    rmfile(agent_config.operation_log_fp)





