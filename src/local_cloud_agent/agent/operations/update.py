import aiofile
import pygit2
from cumulonimbus_models.operations import OperationResult, OperationResultStatus
from common.configuration import agent_config
from agent.post_config import logger
from agent.models import AgentOperation, AgentOperationResult
from agent.util import write_data_to_file, fetch_file_data
from common import constants, git_common, systemd


async def check_systemd_service() -> None:
    logger.info('Checking Systemd Service')
    ref_systemd_conf = constants.service_file_data
    repo_systemd_conf = await fetch_file_data(agent_config.installed_service_fp)

    if ref_systemd_conf != repo_systemd_conf:
        logger.info('Found updated Systemd Service File')
        await systemd_update()
    else:
        logger.info('Systemd Service File is up to date')


async def systemd_update() -> None:
    logger.info('Updating Systemd Service File')
    async with aiofile.async_open(agent_config.installed_service_fp, 'w') as service_file:
        await service_file.write(constants.service_file_data)
    systemd.reload_systemd()


async def reload() -> None:
    systemd.reload_systemd()


async def update_repository(operation: AgentOperation) -> AgentOperationResult:
    logger.info('Updating Repository')
    await write_data_to_file(agent_config.update_operation_fp, operation.model_dump_json())

    repo = pygit2.Repository(agent_config.repo_dir)

    remote = repo.remotes["origin"]
    remote.fetch()
    latest_version = git_common.get_latest_available_version()
    repo.checkout(f'refs/tags/{latest_version}')
    return AgentOperationResult(
        operation_result=OperationResult(
            operation_output='SUCCESS',
            operation_status=OperationResultStatus.SUCCESS
        ), post_op=reload
    )

