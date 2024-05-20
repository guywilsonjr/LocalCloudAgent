import os
from datetime import datetime
from typing import Optional

import aiohttp
from cumulonimbus_models.operations import Operation, OperationResult, OperationResultStatus, OperationType, UpdateOperationResultRequest
from types_aiobotocore_sqs.type_defs import MessageTypeDef

from models import PersistedOperation
from util import agent_state, append_data_to_file, fetch_file_data, local_cloud_agent_dir, logger
from updater import initiate_update_service, update_repo_and_docker_image


operation_status_fp = f'{local_cloud_agent_dir}/operations.log'
update_operation_fp = f'{local_cloud_agent_dir}/operations/update.json'

operations_map = {
    OperationType.UPDATE: update_repo_and_docker_image
}


async def init_operation(message: MessageTypeDef) -> PersistedOperation:
    operation = Operation.parse_raw(message['Body'])
    initiated_operation = PersistedOperation(started=datetime.now(), operation=operation, status=OperationResultStatus.PENDING)
    await append_data_to_file(operation_status_fp, initiated_operation.model_dump_json() + '\n')
    return initiated_operation


async def send_operation_result(operation: PersistedOperation, output: str) -> None:
    update_result_req = UpdateOperationResultRequest(
        agent_id=agent_state.agent_id,
        operation_id=operation.operation.id,
        result=OperationResult(output=output, status=operation.status)
    )
    url = update_result_req.get_url()
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=operation.model_dump()) as resp:
            if resp.status != 200:
                logger.error(f'Failed to send operation result: {resp.status} - {await resp.text()}')


async def complete_operation(operation: PersistedOperation, output: str) -> None:
    await append_data_to_file(operation_status_fp, operation.model_dump_json() + '\n')
    await send_operation_result(operation, output)


async def fetch_update_operation() -> Optional[PersistedOperation]:
    data = await fetch_file_data(update_operation_fp)
    if data is not None:
        os.remove(update_operation_fp)
        return PersistedOperation.parse_raw(data)
    else:
        return None


