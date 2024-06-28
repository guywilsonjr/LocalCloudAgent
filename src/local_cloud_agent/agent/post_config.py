import json
import logging
import sys
from aws_lambda_powertools import Logger
from agent.configuration import agent_config


def serialize_log(json_data: dict) -> str:
    return json.dumps(json_data, indent=2)


logger = Logger(
    service='LocalCloudAgent',
    level=logging.INFO,
    logger_handler=logging.FileHandler(agent_config.agent_log_fp),
    log_uncaught_exceptions=True,
    json_serializer=serialize_log
)
logger.addHandler(logging.StreamHandler(sys.stdout))
