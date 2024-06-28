import json
from datetime import datetime

import aiohttp
from cumulonimbus_models.operations import OperationResult, UpdateOperationResultRequest

from agent.post_config import logger
from agent.models import AgentState, PersistedOperation
from agent.util import BASE_API_URL


async def send_operation_result(agent_state: AgentState, operation: PersistedOperation, output: OperationResult) -> None:
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

