from datetime import datetime

import pytest
from types_aiobotocore_sqs.type_defs import MessageTypeDef
from cumulonimbus_models.operations import OperationResultStatus

from agent.models import AgentOperation
from common.configuration import agent_config
from tests.common_test import test_constants


@pytest.mark.usefixtures("root_fakefs", "fake_base_fs", "installed", "registered_agent")
@pytest.mark.asyncio
async def test_init_operation():
    start_dt = datetime.now()

    test_persist_op = AgentOperation(
        started=datetime.now(),
        operation=test_constants.test_op,
        status=OperationResultStatus.PENDING
    )
    with open(agent_config.operation_log_fp, 'w') as f:
        f.write(test_persist_op.model_dump_json() + '\n')
    from agent.operations import util
    test_msg = MessageTypeDef(
        MessageId='test-message-id',
        Body=test_constants.test_op.model_dump_json()
    )
    await util.init_operation(test_msg)
    with open(agent_config.operation_log_fp, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 2
    persisted_op = AgentOperation.model_validate_json(lines[0].strip())
    assert OperationResultStatus.PENDING == persisted_op.status
    assert test_constants.test_op == persisted_op.operation
    assert start_dt < persisted_op.started





