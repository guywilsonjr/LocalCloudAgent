import os
from datetime import datetime

from cumulonimbus_models.operations import OperationResultStatus

from operations import complete_operation, fetch_update_operation
from util import logger
from updater import fetch_prev_run_version, save_latest_running_version


async def check_for_update_operations() -> None:
    version = os.environ['VERSION']
    prev_version = await fetch_prev_run_version()
    update_operation = await fetch_update_operation()
    if update_operation:
        if prev_version == version:
            final_status = OperationResultStatus.FAILURE
            completed = None
        else:
            final_status = OperationResultStatus.SUCCESS
            completed = datetime.now()

        final_operation = update_operation.copy(
            update={
                'status': final_status,
                'completed': completed
            }
        )
        await complete_operation(final_operation, version)


async def startup():
    version = os.environ['VERSION']
    logger.info(f'Starting agent version: {version}')
    await check_for_update_operations()
    await save_latest_running_version()
