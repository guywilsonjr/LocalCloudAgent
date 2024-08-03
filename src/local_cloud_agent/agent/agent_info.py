import logging
import os
import socket

import aiohttp
from cumulonimbus_models.agent import AgentRegisterRequest, AgentRegisterResponse
from tenacity import before_log, retry, wait_exponential
from local_cloud_agent.common.configuration import agent_config
from local_cloud_agent.agent.models import AgentState
from local_cloud_agent.agent.post_config import logger
from local_cloud_agent.agent.util import BASE_API_URL, fetch_file_data, write_data_to_file


async def register_agent_request(req: AgentRegisterRequest) -> AgentRegisterResponse:
    return AgentRegisterResponse(agent_id='TODO', agent_key='dd', operations_queue_url='TODO', ip_address='TODO')
"""
#@retry(wait=wait_exponential(), before=before_log(logger._logger, logging.INFO))
async def register_agent_requester(req: AgentRegisterRequest) -> AgentRegisterResponse:
    url = AgentRegisterRequest.get_url(BASE_API_URL)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=req.model_dump()) as resp:
            if resp.status != 200:
                err = RuntimeError(f'Failed to register agent: {resp.status} - {await resp.text()}')
                logger.exception(err)
                raise err
            return AgentRegisterResponse(**(await resp.json()))
"""

async def register_agent() -> AgentRegisterResponse:
    hostname = socket.gethostname()
    register_req = AgentRegisterRequest(hostname=hostname)
    agent_data = await register_agent_request(register_req)
    await write_data_to_file(agent_config.agent_registration_fp, agent_data.model_dump_json())
    return agent_data


async def get_registration() -> AgentRegisterResponse:
    agent_data = await fetch_file_data(agent_config.agent_registration_fp)
    if agent_data is None:
        logger.info(f'No registration found at: {agent_config.agent_registration_fp}. Registering agent. Found: {os.listdir(agent_config.agent_dir)}')
        registration = await register_agent()
        logger.info(f'Registration complete for agent: {registration.agent_id}')
        return registration
    else:
        registration = AgentRegisterResponse.model_validate_json(agent_data)
        logger.info(f'Found registration for agent: {registration.agent_id}')
        return registration


async def get_agent_state() -> AgentState:
    agent_registration = await get_registration()
    # TODO
    return AgentState(
        agent_id=agent_registration.agent_id,
        queue_url=agent_registration.operations_queue_url,
        version='TODO'
    )
