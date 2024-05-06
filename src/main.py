import asyncio
import logging
import os.path
import socket
from typing import Dict, List, Optional

import aiohttp
from aiofile import async_open
import aioboto3
from tenacity import before_log, retry, wait_exponential

from routes import get_routes
from cumulonimbus_models.agent import AgentRegisterRequest, AgentRegisterResponse
from cumulonimbus_models.network import NetworkInterface, Gateway, Subnet, GatewaySubnetConnection

from util import home_dir, logger


agent_fp = f'{home_dir}/.local_cloud_agent/agent.json'
aiosession = aioboto3.Session()


def process_ifc(ifc_name: str, routes: list[dict[str, str]]) -> NetworkInterface:
    gateway_routes = [route for route in routes if route['gateway_addr'] != '0.0.0.0']
    default_gateway = None
    if gateway_routes:
        default_gateway_route = [gateway_route for gateway_route in gateway_routes if gateway_route['subnet_addr'] == '0.0.0.0'][0]
        default_gateway = Gateway(address=default_gateway_route['gateway_addr'], name=default_gateway_route['gateway_hostname'])
    gateways = [Gateway(address=gwr['gateway_addr'], name=gwr['gateway_hostname']) for gwr in gateway_routes]
    subnets = [Subnet(address=subnet_route['subnet_addr'], mask=subnet_route['mask_addr']) for subnet_route in routes]

    dest_gateway_name_map = {
        '0.0.0.0': 'default',
        **{
            gwr['subnet_addr']: gwr['gateway_hostname'] for gwr in gateway_routes
        }
    }

    ifc_gateway_subnet_cons = [
        GatewaySubnetConnection(
            gateway_network=dest_gateway_name_map[route['gateway_addr']],
            gateway=Gateway(address=route['gateway_addr'], name=route['gateway_hostname']),
            subnet=Subnet(
                address=route['subnet_addr'],
                mask=route['mask_addr']
            )
        )
        for route in routes if route['gateway_addr'] in dest_gateway_name_map
    ]

    return NetworkInterface(
        ifc_name=ifc_name,
        gateways=gateways,
        subnets=subnets,
        gateway_subnet_connections=ifc_gateway_subnet_cons,
        default_gateway=default_gateway
    )



def process_routes(routes: List[Dict[str, str]]) -> list[NetworkInterface]:
    ifc_names = {route['ifc_name'] for route in routes}
    return [
        process_ifc(ifc_name, [route for route in routes if route['ifc_name'] == ifc_name])
        for ifc_name in ifc_names
    ]


async def get_network_interfaces() -> list[NetworkInterface]:
    routes = await get_routes()
    return process_routes(routes)


@retry(wait=wait_exponential(), before=before_log(logger, logging.INFO))  # type: ignore
async def register_agent_request(data: AgentRegisterRequest) -> AgentRegisterResponse:
    url = 'https://api.local.guywilsonjr.com/agent/register'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data.model_dump()) as resp:
            if resp.status != 200:
                err = RuntimeError(f'Failed to register agent: {resp.status} - {await resp.text()}')
                logger.exception(err)
                raise err
            return AgentRegisterResponse(**(await resp.json()))


async def fetch_file_data(fp: str) -> Optional[str]:
    if os.path.exists(fp):
        async with async_open(fp, 'r') as f:
            return await f.read()
    else:
        return None




async def register_agent() -> AgentRegisterResponse:
    hostname = socket.gethostname()
    register_req = AgentRegisterRequest(hostname=hostname)
    agent_data = await register_agent_request(register_req)
    async with async_open(agent_fp, 'w') as f:
        await f.write(agent_data.model_dump_json())
    return agent_data



def process_message(message: dict[str, str]) -> None:
    logger.info(message)



async def listen_to_queue(agent_data: AgentRegisterResponse) -> None:
    logger.info('Listening to queue')
    async with aiosession.client('sqs') as sqs:
        queue_url = agent_data.operations_queue_url
        while True:
            response = await sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20
            )
            if 'Messages' in response:
                logger.info('Received message')
                message = response['Messages'][0]
                try:
                    process_message(message)
                except Exception as e:
                    logger.exception(e)
                await sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
            else:
                await asyncio.sleep(60 * 60)


async def get_registration() -> AgentRegisterResponse:
    agent_data = await fetch_file_data(agent_fp)
    if agent_data is None:
        logger.info('No registration found, registering agent')
        registration = await register_agent()
        logger.info(f'Registration complete for agent: {registration.agent_id}')
        return registration
    else:
        registration = AgentRegisterResponse.parse_raw(agent_data)
        logger.info(f'Found registration for agent: {registration.agent_id}')
        return registration


async def async_main() -> None:
    agent_registration = await get_registration()
    await listen_to_queue(agent_registration)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()

