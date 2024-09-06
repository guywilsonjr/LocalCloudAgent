from cumulonimbus_models.operations import OperationResult, OperationResultStatus, OperationResultStatuses

import local_cloud_agent
from local_cloud_agent.agent.operations.util import complete_operation
from local_cloud_agent.common.configuration import agent_config
from local_cloud_agent.agent.models import AgentOperation, AgentState
from local_cloud_agent.common.configuration import logger
from local_cloud_agent.agent.util import fetch_file_data


async def check_for_updates(agent_state: AgentState) -> None:
    update_data_str = await fetch_file_data(agent_config.update_operation_fp)
    if update_data_str:
        operation = AgentOperation.model_validate_json(update_data_str)
        logger.info('Found Update Operation')
        logger.info(operation)

        result = OperationResult(
            operation_output='SUCCESS',
            operation_status=OperationResultStatuses.SUCCESS
        )
        await complete_operation(agent_state, operation, result)


async def startup(agent_state: AgentState) -> None:
    logger.info(f'Starting Local Cloud Agent version: {local_cloud_agent.__version__}')
    await check_for_updates(agent_state)




