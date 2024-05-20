import asyncio
import logging
import os
import sys
from socket import socket
from typing import Optional

import aioboto3
import aiohttp
from aiofile import async_open
from aws_lambda_powertools import Logger
from cumulonimbus_models.agent import AgentRegisterRequest, AgentRegisterResponse

from models import AgentState


home_dir = os.environ['HOME']
local_cloud_agent_dir = f'{home_dir}/.local_cloud_agent'
os.makedirs(local_cloud_agent_dir, exist_ok=True)

logger = Logger(
    service='LocalCloudAgent',
    logger_handler=logging.FileHandler(f'{home_dir}/.local_cloud_agent/agent.log'),
    log_uncaught_exceptions=True
)
logger.addHandler(logging.StreamHandler(sys.stdout))

if not os.path.exists(f'{home_dir}/.aws/credentials'):
    logger.error('AWS credentials not found. Please run `aws configure` to set up your credentials.')
    exit(1)


aiosession: aioboto3.Session = aioboto3.Session()

agent_registration_fp = f'{local_cloud_agent_dir}/agent/registration.json'
BASE_API_URL = 'https://api.local.guywilsonjr.com'


@retry(wait=wait_exponential(), before=before_log(logger, logging.INFO))  # type: ignore
async def register_agent_request(req: AgentRegisterRequest) -> AgentRegisterResponse:
    url = req.get_url(BASE_API_URL)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=req.model_dump()) as resp:
            if resp.status != 200:
                err = RuntimeError(f'Failed to register agent: {resp.status} - {await resp.text()}')
                logger.exception(err)
                raise err
            return AgentRegisterResponse(**(await resp.json()))


async def register_agent() -> AgentRegisterResponse:
    hostname = socket.gethostname()
    register_req = AgentRegisterRequest(hostname=hostname)
    agent_data = await register_agent_request(register_req)
    await write_data_to_file(agent_registration_fp, agent_data.model_dump_json())
    return agent_data


async def get_registration() -> AgentRegisterResponse:
    agent_data = await fetch_file_data(agent_registration_fp)
    if agent_data is None:
        logger.info('No registration found, registering agent')
        registration = await register_agent()
        logger.info(f'Registration complete for agent: {registration.agent_id}')
        return registration
    else:
        registration = AgentRegisterResponse.parse_raw(agent_data)
        logger.info(f'Found registration for agent: {registration.agent_id}')
        return registration


agent_registration = asyncio.run(get_registration())

agent_state = AgentState(
    agent_id=agent_registration.agent_id,
    queue_url=agent_registration.operations_queue_url,
    version=os.environ['VERSION']
)


async def fetch_file_data(fp: str) -> Optional[str]:
    if os.path.exists(fp):
        async with async_open(fp, 'r') as f:
            return await f.read()
    else:
        return None


async def write_data_to_file(fp: str, data: str) -> None:
    async with async_open(fp, 'w') as f:
        await f.write(data)


async def append_data_to_file(fp: str, data: str) -> None:
    async with async_open(fp, 'a') as f:
        await f.write(data)
