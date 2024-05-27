import os
from datetime import datetime

from cumulonimbus_models.operations import OperationResultStatus
from git import Git

from operations import complete_operation, fetch_update_operation
from constants import repo_url
from util import logger
from updater import save_latest_running_version


def get_latest_available_version() -> str:
    git_cmd = Git()
    resp = git_cmd.ls_remote(repo_url, sort='v:refname')
    resp_lines = resp.split('\n')
    valid_entries = [l for l in resp_lines if '{}' not in l and 'HEAD' not in l]
    latest_entry = valid_entries[-1]
    ref_entry = latest_entry.split('\t')[-1]
    version = ref_entry.split('/')[-1]
    return version



async def check_for_update_operations() -> None:
    version = os.environ['VERSION']
    latest_version = get_latest_available_version()
    logger.info(f'Current Version: {version}')
    logger.info(f'Latest Available Version: {latest_version}')
    update_operation = await fetch_update_operation()
    if update_operation:
        if version == latest_version:
            logger.info('Update Completed')
            final_status = OperationResultStatus.SUCCESS
            completed = datetime.now()
        else:
            logger.info('Update Failed')
            final_status = OperationResultStatus.FAILURE
            completed = None

        final_operation = update_operation.copy(
            update={
                'status': final_status,
                'completed': completed
            }
        )
        await complete_operation(final_operation, version)


async def startup():
    version = os.environ['VERSION']
    logger.info(os.environ)
    logger.info(f'Starting agent version: {version}')
    await check_for_update_operations()
    await save_latest_running_version()
