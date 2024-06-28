import logging
import os
import socket

import aiohttp
from cumulonimbus_models.agent import AgentRegisterRequest, AgentRegisterResponse
from tenacity import before_log, retry, wait_exponential
from agent.initialize import logger
from agent.configuration import agent_config
from agent.models import AgentState
from agent.util import BASE_API_URL, fetch_file_data, write_data_to_file
from agent.versioning import get_latest_tag


async def startup():
    version = get_latest_tag().name
    logger.info(f'Starting Local Cloud Agent version: {version}')
    logger.info(f'Using Agent Config:')
    logger.info(agent_config.model_dump())


@retry(wait=wait_exponential(), before=before_log(logger, logging.INFO))
async def register_agent_request(req: AgentRegisterRequest) -> AgentRegisterResponse:
    url = AgentRegisterRequest.get_url(BASE_API_URL)
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
    await write_data_to_file(agent_config.agent_registration_fp, agent_data.model_dump_json())
    return agent_data


async def get_registration() -> AgentRegisterResponse:
    agent_data = await fetch_file_data(agent_config.agent_registration_fp)
    if agent_data is None:
        logger.info(f'No registration found, registering agent. Found: {os.listdir(agent_config.agent_dir)}')
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
        version=get_latest_tag().name
    )
