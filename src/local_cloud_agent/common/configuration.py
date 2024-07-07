# Must use minimal imports to avoid circular imports

import os

from pydantic import BaseModel
from common import constants


class AgentConfig(BaseModel):

    @property
    def home_dir(self) -> str:
        return constants.root_dir

    @property
    def log_dir(self) -> str:
        return f'{constants.install_log_dir}'

    @property
    def aws_dir(self) -> str:
        return f'{constants.aws_dir}'

    @property
    def repo_dir(self) -> str:
        return f'{constants.installed_repo_dir}'

    @property
    def metadata_dir(self) -> str:
        return f'{constants.metadata_dir}'

    @property
    def agent_dir(self) -> str:
        return f'{constants.metadata_dir}/agent'

    @property
    def operations_dir(self) -> str:
        return f'{constants.metadata_dir}/operations'

    @property
    def aws_creds_fp(self) -> str:
        return f'{constants.aws_dir}/credentials'

    @property
    def agent_registration_fp(self) -> str:
        return f'{self.agent_dir}/registration.json'

    @property
    def agent_log_fp(self) -> str:
        return f'{constants.install_log_dir}/local_cloud_agent.log'

    @property
    def operation_log_fp(self) -> str:
        return f'{self.operations_dir}/operations.log'

    @property
    def update_operation_fp(self) -> str:
        return f'{self.operations_dir}/update.json'

    @property
    def repo_service_fp(self) -> str:
        return f'{"/".join([self.repo_dir, constants.relative_repo_service_fp])}'

    @property
    def installed_service_fp(self) -> str:
        return f'{constants.installed_service_conf_fp}'


agent_config = AgentConfig()


def ensure_dirs_exist():
    os.makedirs(agent_config.metadata_dir, exist_ok=True)
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