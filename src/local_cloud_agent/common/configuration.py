# Must use minimal imports to avoid circular imports

import os
from typing import ClassVar

import yaml
from pydantic import BaseModel
from common import constants


fs_root_path = os.environ.get('FS_ROOT_PATH', '')


class AgentConfig(BaseModel):
    fs_root_path: ClassVar[str] = os.environ.get('FS_ROOT_PATH', '')

    @property
    def home_dir(self) -> str:
        return f'{self.fs_root_path}{constants.root_dir}'

    @property
    def log_dir(self) -> str:
        return f'{self.fs_root_path}{constants.install_log_dir}'

    @property
    def aws_dir(self) -> str:
        return f'{self.fs_root_path}{constants.aws_dir}'

    @property
    def repo_dir(self) -> str:
        return f'{self.fs_root_path}{constants.installed_repo_dir}'

    @property
    def metadata_dir(self) -> str:
        return f'{self.fs_root_path}{constants.metadata_dir}'

    @property
    def agent_dir(self) -> str:
        return f'{self.fs_root_path}{constants.metadata_dir}/agent'

    @property
    def operations_dir(self) -> str:
        return f'{self.fs_root_path}{constants.metadata_dir}/operations'

    @property
    def aws_creds_fp(self) -> str:
        return f'{self.fs_root_path}{constants.aws_dir}/credentials'

    @property
    def agent_registration_fp(self) -> str:
        return f'{self.agent_dir}/registration.json'

    @property
    def agent_log_fp(self) -> str:
        print('root path at agent log fp', self.fs_root_path)
        return f'{self.fs_root_path}{constants.install_log_dir}/local_cloud_agent.log'

    @property
    def operation_log_fp(self) -> str:
        return f'{self.operations_dir}/operations.log'

    @property
    def update_operation_fp(self) -> str:
        return f'{self.operations_dir}/update.json'

    @property
    def repo_service_fp(self) -> str:
        return f'{"/".join([self.repo_dir, constants.repo_service_fp])}'

    @property
    def installed_service_fn(self) -> str:
        return f'{self.fs_root_path}{constants.service_fn}'


conf_path = os.environ.get('LOCAL_CLOUD_AGENT_CONF_PATH', constants.install_conf_fp)
with open(conf_path, 'r') as conf_file:
    conf = yaml.safe_load(conf_file)


agent_config = AgentConfig(**conf)
