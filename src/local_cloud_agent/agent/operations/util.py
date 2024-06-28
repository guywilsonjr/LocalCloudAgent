from datetime import datetime

from cumulonimbus_models.operations import Operation, OperationResult, OperationResultStatus
from types_aiobotocore_sqs.type_defs import MessageTypeDef
from agent.models import PersistedOperation
from agent.configuration import agent_config
from agent.util import append_data_to_file


async def init_operation(message: MessageTypeDef) -> PersistedOperation:
    operation = Operation.model_validate_json(message['Body'])
    initiated_operation = PersistedOperation(started=datetime.now(), operation=operation, status=OperationResultStatus.PENDING)
    await append_data_to_file(agent_config.operation_log_fp, initiated_operation.model_dump_json() + '\n')
    return initiated_operation

