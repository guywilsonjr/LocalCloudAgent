import json
import logging
import os
import sys
from typing import Any

from aws_lambda_powertools import Logger
from pydantic.main import BaseModel
from local_cloud_agent.common import constants



class AgentConfig(BaseModel):

    @property
    def prefix(self) -> str:
        return os.environ.get(constants.prefix_env_var, '')


    def get_prefixed_dir(self, dir_name: str) -> str:
        return f'{self.prefix.rstrip("/")}/{dir_name.lstrip("/")}'

    @property
    def log_dir(self) -> str:
        return self.get_prefixed_dir(constants.install_log_dir)

    @property
    def aws_dir(self) -> str:
        return self.get_prefixed_dir(constants.aws_dir)


    @property
    def metadata_dir(self) -> str:
        return self.get_prefixed_dir(constants.metadata_dir)

    @property
    def conf_dir(self) -> str:
        return self.get_prefixed_dir(constants.install_agent_conf_dir)

    @property
    def agent_dir(self) -> str:
        return f'{self.metadata_dir}/agent'

    @property
    def operations_dir(self) -> str:
        return f'{self.metadata_dir}/operations'

    @property
    def aws_creds_fp(self) -> str:
        return f'{self.aws_dir}/credentials'

    @property
    def agent_registration_fp(self) -> str:
        return f'{self.agent_dir}/registration.json'

    @property
    def agent_log_fp(self) -> str:
        return f'{self.log_dir}/local_cloud_agent.log'

    @property
    def operation_log_fp(self) -> str:
        return f'{self.operations_dir}/operations.log'

    @property
    def update_operation_fp(self) -> str:
        return f'{self.operations_dir}/update.json'

    @property
    def installed_service_conf_dir(self) -> str:
        return self.get_prefixed_dir(constants.installed_service_conf_dir)

    @property
    def installed_service_fp(self) -> str:
        return f'{self.installed_service_conf_dir}/{constants.installed_service_conf_fn}'



agent_config = AgentConfig()


def ensure_dirs_exist() -> None:
    os.makedirs(agent_config.metadata_dir, exist_ok=True)
    os.makedirs(agent_config.agent_dir, exist_ok=True)
    os.makedirs(agent_config.operations_dir, exist_ok=True)


def validate_fs() -> None:
    ensure_dirs_exist()
    if not os.path.exists(agent_config.aws_creds_fp):
        base_msg = 'AWS credentials not found. Please run `aws configure` to set up your credentials.'
        home_msg = f'Could not find {agent_config.aws_creds_fp}'
        msg = '\n'.join([base_msg, home_msg])
        raise RuntimeError(msg)


def serialize_log(json_data: dict[str, Any]) -> str:
    return json.dumps(json_data, indent=2)


log_dir_exists = os.path.exists(agent_config.log_dir)
if log_dir_exists:
    logger = Logger(
        service='LocalCloudAgent',
        level=logging.INFO,
        logger_handler=logging.FileHandler(agent_config.agent_log_fp),
        log_uncaught_exceptions=True,
        json_serializer=serialize_log
    )
else:
    logger = logging.getLogger(__name__)


logger.addHandler(logging.StreamHandler(sys.stdout))

if not log_dir_exists:
    logger.warning(f'Log directory not found: {agent_config.log_dir}. Logging to stdout only.')