import json
from datetime import datetime

import aiohttp
from cumulonimbus_models.operations import Operation, OperationResult, OperationResultStatuses, UpdateOperationResultRequest
from types_aiobotocore_sqs.type_defs import MessageTypeDef
from local_cloud_agent.agent.models import AgentOperation, AgentState
from local_cloud_agent.common.configuration import agent_config, logger
from local_cloud_agent.agent.util import append_data_to_file


async def init_operation(message: MessageTypeDef) -> AgentOperation:
    operation = Operation.model_validate_json(message['Body'])
    initiated_operation = AgentOperation(started=datetime.now(), operation=operation, status=OperationResultStatuses.PENDING)
    await append_data_to_file(agent_config.operation_log_fp, initiated_operation.model_dump_json() + '\n')
    return initiated_operation


async def send_operation_result(agent_state: AgentState, operation: AgentOperation, output: OperationResult) -> None:
    update_result_req = UpdateOperationResultRequest(
        started=operation.started,
        operation_result=output,
        completed=datetime.now()
    )
    url = UpdateOperationResultRequest.get_url(url_data=dict(agent_id=agent_state.agent_id, operation_id=operation.operation.id))
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=json.loads(update_result_req.model_dump_json())) as resp:
            if resp.status != 200:
                logger.error(f'Failed to send operation result: {resp.status} - {await resp.text()}')


async def complete_operation(agent_state: AgentState, operation: AgentOperation, output: OperationResult) -> None:
    await append_data_to_file(agent_config.operation_log_fp, operation.model_dump_json() + '\n')
    await send_operation_result(agent_state, operation, output)
