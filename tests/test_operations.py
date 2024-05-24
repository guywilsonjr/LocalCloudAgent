import os
from datetime import datetime

import pytest
from types_aiobotocore_sqs.type_defs import MessageTypeDef
from cumulonimbus_models.operations import Operation, OperationResultStatus, OperationType

from models import PersistedOperation
import constants
from test_common import setup_home_dir, rmfile


test_op = Operation(
    id='test-operation-id',
    type=OperationType.UPDATE,
    parameters={},
)


@pytest.mark.asyncio
async def test_init_operation(setup_home_dir):
    start_dt = datetime.now()

    test_persist_op = PersistedOperation(
        started=datetime.now(),
        operation=test_op,
        status=OperationResultStatus.PENDING
    )
    with open(constants.operation_log_fp, 'w') as f:
        f.write(test_persist_op.model_dump_json() + '\n')
    import operations

    test_msg = MessageTypeDef(
        MessageId='test-message-id',
        Body=test_op.model_dump_json()
    )
    await operations.init_operation(test_msg)
    with open(constants.operation_log_fp, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 2
    persisted_op = PersistedOperation.model_validate_json(lines[0].strip())
    assert OperationResultStatus.PENDING == persisted_op.status
    assert test_op == persisted_op.operation
    assert start_dt < persisted_op.started
    rmfile(constants.operation_log_fp)


