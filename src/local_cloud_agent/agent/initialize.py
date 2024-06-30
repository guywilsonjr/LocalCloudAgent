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
    logger.info(f'Using Agent Config:')
    logger.info(agent_config.model_dump())
    await check_for_updates()


def ensure_dirs_exist():
    os.makedirs(agent_config.metadata_dir, exist_ok=True)
    os.makedirs(agent_config.agent_dir, exist_ok=True)
    os.makedirs(agent_config.operations_dir, exist_ok=True)


def validate_fs():
    ensure_dirs_exist()
    if not os.path.exists(agent_config.repo_dir):
        raise RuntimeError(f'Repo dir not found: {agent_config.repo_dir}')

    if not os.path.exists(agent_config.aws_creds_fp):
        base_msg = 'AWS credentials not found. Please run `aws configure` to set up your credentials.'
        home_msg = f'Could not find {agent_config.aws_creds_fp}'
        msg = '\n'.join([base_msg, home_msg])
        raise RuntimeError(msg)



