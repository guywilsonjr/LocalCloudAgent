import shutil
from git import Repo
from cumulonimbus_models.operations import OperationResult, OperationResultStatus
from local_cloud_agent.agent.configuration import agent_config
from local_cloud_agent.agent.initialize import logger
from local_cloud_agent.agent.models import PersistedOperation
from local_cloud_agent.agent.util import write_data_to_file, fetch_file_data
from local_cloud_agent.common import constants, systemd


async def check_systemd_service():
    logger.info('Checking Systemd Service')
    ref_systemd_conf = await fetch_file_data('/'.join([agent_config.repo_dir, constants.relative_service_file_path]))
    repo_systemd_conf = await fetch_file_data(constants.service_fn)
    if ref_systemd_conf != repo_systemd_conf:
        logger.info('Found updated Systemd Service File')
        await systemd_update()
    else:
        logger.info('Systemd Service File is up to date')


async def systemd_update():
    logger.info('Updating Systemd Service File')
    ref_conf_path = '/'.join([agent_config.repo_dir, constants.relative_service_file_path])
    shutil.copyfile(ref_conf_path, constants.service_fn)
    systemd.reload_systemd()


async def update_repository(operation: PersistedOperation) -> OperationResult:
    logger.info('Updating Repository')
    #TODO ACTUALLY READ FROM THIS FILE and finish sytemd stuff
    await write_data_to_file(agent_config.update_operation_fp, operation.model_dump_json())

    repo = Repo(agent_config.repo_dir)
    remote = repo.remote()
    remote.pull()
    return OperationResult(
        operation_output='SUCCESS',
        operation_status=OperationResultStatus.SUCCESS
    )
