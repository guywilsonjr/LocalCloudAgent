from datetime import datetime

from cumulonimbus_models.operations import Operation, OperationResultStatus
from types_aiobotocore_sqs.type_defs import MessageTypeDef
from local_cloud_agent.agent.models import AgentOperation
from local_cloud_agent.common.configuration import agent_config
from local_cloud_agent.agent.util import append_data_to_file


async def init_operation(message: MessageTypeDef) -> AgentOperation:
    operation = Operation.model_validate_json(message['Body'])
    initiated_operation = AgentOperation(started=datetime.now(), operation=operation, status=OperationResultStatus.PENDING)
    await append_data_to_file(agent_config.operation_log_fp, initiated_operation.model_dump_json() + '\n')
    return initiated_operation

