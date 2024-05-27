import logging
import os
import sys
import socket
from typing import Optional

import aioboto3
import aiohttp
from aiofile import async_open
from aws_lambda_powertools import Logger
from cumulonimbus_models.agent import AgentRegisterRequest, AgentRegisterResponse
from tenacity import before_log, retry, wait_exponential

from constants import agent_dir, agent_log_fp, agent_registration_fp
from models import AgentState


logger = Logger(
    service='LocalCloudAgent',
    logger_handler=logging.FileHandler(agent_log_fp),
    log_uncaught_exceptions=True
)
logger.addHandler(logging.StreamHandler(sys.stdout))

aiosession: aioboto3.Session = aioboto3.Session()

BASE_API_URL = 'https://api.local.guywilsonjr.com'


@retry(wait=wait_exponential(), before=before_log(logger, logging.INFO))
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
    if os.path.exists(fp):
        async with async_open(fp, 'a') as f:
            await f.write(data)
    else:
        await write_data_to_file(fp, data)


async def get_registration() -> AgentRegisterResponse:
    agent_data = await fetch_file_data(agent_registration_fp)
    if agent_data is None:
        logger.info(f'No registration found, registering agent. Found: {os.listdir(agent_dir)}')
        registration = await register_agent()
        logger.info(f'Registration complete for agent: {registration.agent_id}')
        return registration
    else:
        registration = AgentRegisterResponse.model_validate_json(agent_data)
        logger.info(f'Found registration for agent: {registration.agent_id}')
        return registration


async def get_agent_state() -> AgentState:
    agent_registration = await get_registration()
    return AgentState(
        agent_id=agent_registration.agent_id,
        queue_url=agent_registration.operations_queue_url,
        version=os.environ['VERSION']
    )
