import base64
from typing import Tuple

from cumulonimbus_models.operations import OperationResult, OperationResultStatus
from git import Repo
import docker

from constants import repo_dir, update_operation_fp
from models import PersistedOperation
from util import aiosession, logger, write_data_to_file


local_agent_repository_name = '936272581790.dkr.ecr.us-west-1.amazonaws.com/cumulonimbusinfrastructurestackecrb011c8ff-localcloudagent882a885f-uf9f1uyibbfx'


async def update_repository() -> None:
    repo = Repo(repo_dir)
    remote = repo.remote()
    remote.pull()


async def fetch_ecr_auth() -> Tuple[str, str]:
    async with aiosession.client('sts') as sts:
        account_id = (await sts.get_caller_identity())['Account']

    ecr_url = f'{account_id}.dkr.ecr.{aiosession.region_name}.amazonaws.com'
    async with aiosession.client('ecr') as ecr:
        response = await ecr.get_authorization_token()
    auth_data = response['authorizationData'][0]
    token = auth_data['authorizationToken']
    auth_data = base64.b64decode(token).decode()
    return ecr_url, auth_data


async def initiate_update_service() -> None:
    docker_client = docker.from_env()
    ecr_url, auth_data = await fetch_ecr_auth()
    username, password = auth_data.split(':')
    docker_client.login(username=username, password=password, registry=ecr_url)
    docker_client.api.pull(
        repository=local_agent_repository_name,
        tag='latest'
    )


async def update_repo_and_docker_image(operation: PersistedOperation) -> OperationResult:
    logger.info('Updating Repository and Docker Image')
    await write_data_to_file(update_operation_fp, operation.model_dump_json())
    await update_repository()
    await initiate_update_service()
    return OperationResult(
        operation_output='SUCCESS',
        operation_status=OperationResultStatus.SUCCESS
    )

