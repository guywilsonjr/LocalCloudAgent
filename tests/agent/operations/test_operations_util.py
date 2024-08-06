from datetime import datetime

import pytest
from types_aiobotocore_sqs.type_defs import MessageTypeDef
from cumulonimbus_models.operations import OperationResultStatus

from local_cloud_agent.agent.models import AgentOperation
from local_cloud_agent.common.configuration import agent_config
from tests.common_test import eval_constants


@pytest.mark.usefixtures("registered_agent")
@pytest.mark.asyncio
async def test_init_operation():
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





