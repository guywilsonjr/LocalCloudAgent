import logging
import os
import sys

from aws_lambda_powertools import Logger


home_dir = os.environ['HOME']
os.makedirs(f'{home_dir}/.local_cloud_agent', exist_ok=True)

logger = Logger(
    service='LocalCloudAgent',
    logger_handler=logging.FileHandler(f'{home_dir}/.local_cloud_agent/agent.log'),
    log_uncaught_exceptions=True
)
logger.addHandler(logging.StreamHandler(sys.stdout))
