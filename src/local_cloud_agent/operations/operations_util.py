import json
from datetime import datetime

import aiohttp
from cumulonimbus_models.operations import Operation, OperationResult, OperationResultStatus, OperationType, UpdateOperationResultRequest
from types_aiobotocore_sqs.type_defs import MessageTypeDef
from initialize import logger
from agent import get_agent_state
from models import PersistedOperation
from configuration import agent_config
from util import append_data_to_file, BASE_API_URL
from versioning import update_repo_and_docker_image


operations_map = {
    OperationType.UPDATE: update_repo_and_docker_image
}


async def init_operation(message: MessageTypeDef) -> PersistedOperation:
    operation = Operation.model_validate_json(message['Body'])
    initiated_operation = PersistedOperation(started=datetime.now(), operation=operation, status=OperationResultStatus.PENDING)
    await append_data_to_file(agent_config.operation_log_fp, initiated_operation.model_dump_json() + '\n')
    return initiated_operation


async def send_operation_result(operation: PersistedOperation, output: OperationResult) -> None:
    agent_state = await get_agent_state()
    update_result_req = UpdateOperationResultRequest(
        operation_result=output,
        started=operation.started,
        completed=datetime.now()
    )
    url = UpdateOperationResultRequest.get_url(base_url=BASE_API_URL, agent_id=agent_state.agent_id, operation_id=operation.operation.id)
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=json.loads(update_result_req.model_dump_json())) as resp:
            if resp.status != 200:
                logger.error(f'Failed to send operation result: {resp.status} - {await resp.text()}')


async def complete_operation(operation: PersistedOperation, output: OperationResult) -> None:
    await append_data_to_file(agent_config.operation_log_fp, operation.model_dump_json() + '\n')
    await send_operation_result(operation, output)

