import base64
import os
from git import Repo
import docker  # type: ignore

from util import aiosession, fetch_file_data, local_cloud_agent_dir, logger, write_data_to_file


local_agent_repository_name = 'cumulonimbusinfrastructurestackecrb011c8ff-localcloudagent882a885f-uf9f1uyibbfx'
latest_running_version_fp = f'{local_cloud_agent_dir}/latest_running_version'


async def save_latest_running_version() -> None:
    await write_data_to_file(latest_running_version_fp, os.environ['VERSION'])


async def fetch_prev_run_version() -> str:
    return await fetch_file_data(latest_running_version_fp)


def update_repository() -> None:
    pass


async def initiate_update_service() -> None:
    docker_client = docker.from_env()

    async with aiosession.client('sts') as sts:
        account_id = (await sts.get_caller_identity())['Account']

    ecr_url = f'{account_id}.dkr.ecr.{aiosession.region_name}.amazonaws.com'
    async with aiosession.client('ecr') as ecr:
        response = await ecr.get_authorization_token()
    auth_data = response['authorizationData'][0]
    token = auth_data['authorizationToken']
    password = base64.b64decode(token).decode()
    docker_client.login(username='AWS', password=password, registry=ecr_url)
    docker_client.api.pull(
        repository=local_agent_repository_name,
        tag='latest'
    )
    logger.info('Pulled latest image. Restarting')
    exit(0)

