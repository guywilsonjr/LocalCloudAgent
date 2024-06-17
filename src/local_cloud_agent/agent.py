import os

from util import logger


async def startup():
    version = os.environ['VERSION']
    logger.info(os.environ)
    logger.info(f'Starting Local Cloud Agent version: {version}')
