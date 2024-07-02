import os

from cumulonimbus_models.operations import OperationResult, OperationResultStatus

from common.configuration import agent_config
from agent.models import AgentOperation
from agent.operations.post_ops import complete_operation
from agent.post_config import logger
from agent.util import fetch_file_data
from agent.versioning import get_latest_tag


async def check_for_updates() -> None:
    update_data_str = await fetch_file_data(agent_config.update_operation_fp)
    if update_data_str:
        operation = AgentOperation.model_validate_json(update_data_str)
        logger.info('Found Update Operation')
        logger.info(operation)

        result = OperationResult(
            operation_output='SUCCESS',
            operation_status=OperationResultStatus.SUCCESS
        )
        await complete_operation(operation, result)


async def startup():
    version = get_latest_tag().name
    logger.info(f'Starting Local Cloud Agent version: {version}')
    await check_for_updates()




