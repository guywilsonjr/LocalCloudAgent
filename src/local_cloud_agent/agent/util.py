import logging
import os
from typing import Optional

import aioboto3
from aiofile import async_open


aiosession: aioboto3.Session = aioboto3.Session()

BASE_API_URL = 'https://api.local.guywilsonjr.com'


async def fetch_file_data(fp: str) -> Optional[str]:
    if os.path.exists(fp):
        async with async_open(fp, 'r') as f:
            return await f.read()
    else:
        return None


async def write_data_to_file(fp: str, data: str) -> None:
    logging.info(f'Writing data to file: {fp}')
    logging.info(f'In dir: {os.getcwd()}')
    async with async_open(fp, 'w') as f:
        await f.write(data)


async def append_data_to_file(fp: str, data: str) -> None:
    if os.path.exists(fp):
        async with async_open(fp, 'a') as f:
            await f.write(data)
    else:
        await write_data_to_file(fp, data)

