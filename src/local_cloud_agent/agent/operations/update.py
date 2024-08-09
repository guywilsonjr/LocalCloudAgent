from cumulonimbus_models.operations import OperationResult, OperationResultStatus
from local_cloud_agent.common.configuration import agent_config
from local_cloud_agent.common.configuration import logger
from local_cloud_agent.agent.models import AgentOperation, AgentOperationResult
from local_cloud_agent.agent.util import write_data_to_file, fetch_file_data
from local_cloud_agent.common import constants


async def check_systemd_service() -> bool:
    logger.info('Checking Systemd Service')
    ref_systemd_conf = constants.service_file_data
    repo_systemd_conf = await fetch_file_data(agent_config.installed_service_fp)

    if ref_systemd_conf != repo_systemd_conf:
        logger.debug('Found updated Systemd Service File')
        logger.debug(f'Installed config: {repo_systemd_conf}\nReference config: {ref_systemd_conf}')
        return True
    else:
        logger.debug('Systemd Service File is up to date')
        return False


async def reload(operation: AgentOperation) -> None:
    # TODO
    logger.info(f'TODO: Running post operation for operation: {operation}')



async def update() -> None:
    # TODO: STUFF
    pass


async def update_local_cloud_agent(operation: AgentOperation) -> AgentOperationResult:
    logger.info('Updating Local Cloud Agent')
    await write_data_to_file(agent_config.update_operation_fp, operation.model_dump_json())
    await update()
    return AgentOperationResult(
        operation_result=OperationResult(
            operation_output='SUCCESS',
            operation_status=OperationResultStatus.SUCCESS
        ), post_op=reload
    )

