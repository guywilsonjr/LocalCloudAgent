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

from configuration import agent_config
from models import AgentState


logger = Logger(
    service='LocalCloudAgent',
    logger_handler=logging.FileHandler(agent_config.agent_log_fp),
    log_uncaught_exceptions=True
)
logger.addHandler(logging.StreamHandler(sys.stdout))

aiosession: aioboto3.Session = aioboto3.Session()

BASE_API_URL = 'https://api.local.guywilsonjr.com'



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

