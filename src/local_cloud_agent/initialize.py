import logging
import os
import sys

from aws_lambda_powertools import Logger

from configuration import agent_config


def ensure_dirs_exist():
    os.makedirs(agent_config.local_cloud_agent_dir, exist_ok=True)
    os.makedirs(agent_config.agent_dir, exist_ok=True)
    os.makedirs(agent_config.operations_dir, exist_ok=True)


def validate_fs():
    ensure_dirs_exist()
    if not os.path.exists(agent_config.repo_dir):
        raise RuntimeError(f'Repo dir not found: {agent_config.repo_dir}')

    if not os.path.exists(agent_config.aws_creds_fp):
        base_msg = 'AWS credentials not found. Please run `aws configure` to set up your credentials.'
        home_msg = f'Could not find {agent_config.aws_creds_fp}'
        msg = '\n'.join([base_msg, home_msg])
        raise RuntimeError(msg)


logger = Logger(
    service='LocalCloudAgent',
    level=logging.INFO,
    logger_handler=logging.FileHandler(agent_config.agent_log_fp),
    log_uncaught_exceptions=True
)
logger.addHandler(logging.StreamHandler(sys.stdout))

