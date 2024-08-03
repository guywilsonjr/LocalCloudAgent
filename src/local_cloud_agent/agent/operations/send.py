import json
from datetime import datetime

import aiohttp
from cumulonimbus_models.operations import OperationResult, UpdateOperationResultRequest

from local_cloud_agent.agent.post_config import logger
from local_cloud_agent.agent.models import AgentState, AgentOperation
from local_cloud_agent.agent.util import BASE_API_URL
from typing import Any
#TODO
async def send_operation_result(a: Any, b: Any, c: Any) -> None:
    return None
"""
async def send_operation_results(agent_state: AgentState, operation: AgentOperation, output: OperationResult) -> None:
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
"""
