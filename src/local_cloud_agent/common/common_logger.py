import os
import re

from pydantic import BaseModel
from common import constants


dir_pattern = r'^[\/\w+]+$'
dir_regex = re.compile(dir_pattern)


def get_parent_dir(dir_name: str) -> str:
    dir_name = dir_name.strip()
    if not dir_regex.match(dir_name):
        raise ValueError(f'Invalid dir_name: {dir_name}')
    if dir_name == '/':
        return '/'
    dir_name_parts = dir_name.split('/')
    return '/'.join(dir_name_parts[:-1])


class AgentConfig(BaseModel):

    @property
    def prefix(self) -> str:
        return os.environ.get(constants.prefix_env_var, '')

    def get_prefixed_dir(self, dir_name: str) -> str:
        return f'{self.prefix.rstrip("/")}/{dir_name.lstrip("/")}'

    @property
    def home_dir(self) -> str:
        return self.get_prefixed_dir(constants.root_home_dir)

    @property
    def var_local_dir(self) -> str:
        return self.get_prefixed_dir(constants.var_local_dir)

    @property
    def var_log_dir(self) -> str:
        return self.get_prefixed_dir(constants.var_log_dir)


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
    def etc_dir(self) -> str:
        return self.get_prefixed_dir(constants.etc_dir)

    @property
    def conf_dir(self) -> str:
        return f'{self.etc_dir}/{constants.lower_keyword}'

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
        return f'{self.log_dir}/{constants.lower_keyword}.log'

    @property
    def operation_log_fp(self) -> str:
        return f'{self.operations_dir}/operations.log'

    @property
    def update_operation_fp(self) -> str:
        return f'{self.operations_dir}/update.json'


    @property
    def installed_service_fp(self) -> str:
        return self.get_prefixed_dir(constants.installed_service_conf_fp)



agent_config = AgentConfig()


def ensure_dirs_exist() -> None:
    os.makedirs(agent_config.metadata_dir, exist_ok=True)
    os.makedirs(agent_config.agent_dir, exist_ok=True)
    os.makedirs(agent_config.operations_dir, exist_ok=True)


def validate_fs() -> None:
    ensure_dirs_exist()
    if not os.path.exists(agent_config.repo_dir):
        raise RuntimeError(f'Repo dir not found: {agent_config.repo_dir}')

    if not os.path.exists(agent_config.aws_creds_fp):
        base_msg = 'AWS credentials not found. Please run `aws configure` to set up your credentials.'
        home_msg = f'Could not find {agent_config.aws_creds_fp}'
        msg = '\n'.join([base_msg, home_msg])
        raise RuntimeError(msg)
