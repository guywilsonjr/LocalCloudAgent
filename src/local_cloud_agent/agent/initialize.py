from cumulonimbus_models.operations import OperationResult, OperationResultStatus

from common.configuration import agent_config
from agent.models import AgentOperation, AgentState
from agent.operations.post_ops import complete_operation
from agent.post_config import logger
from agent.util import fetch_file_data


async def check_for_updates(agent_state: AgentState) -> None:
    update_data_str = await fetch_file_data(agent_config.update_operation_fp)
    if update_data_str:
        operation = AgentOperation.model_validate_json(update_data_str)
        logger.info('Found Update Operation')
        logger.info(operation)

        result = OperationResult(
            operation_output='SUCCESS',
            operation_status=OperationResultStatus.SUCCESS
        )
        await complete_operation(agent_state, operation, result)


async def startup(agent_state: AgentState) -> None:
    # TODO
    version = """TODO"""
    logger.info(f'Starting Local Cloud Agent version: {version}')
    await check_for_updates(agent_state)




