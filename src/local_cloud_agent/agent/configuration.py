# Must use minimal imports to avoid circular imports
import os
import yaml
from pydantic import BaseModel, Field
from common import constants


fs_root_path = os.environ.get('FS_ROOT_PATH', '')


class AgentConfig(BaseModel):
    home_dir: str = f'{fs_root_path}{constants.root_dir}'
    log_dir: str = f'{fs_root_path}{constants.install_log_dir}'
    aws_dir: str = f'{fs_root_path}{constants.aws_dir}'
    repo_dir: str = f'{fs_root_path}{constants.installed_repo_dir}'
    fs_root_path: str = fs_root_path


    metadata_dir: str = f'{fs_root_path}{constants.metadata_dir}'
    agent_dir: str = f'{fs_root_path}{constants.metadata_dir}/agent'
    operations_dir: str = f'{fs_root_path}{constants.metadata_dir}/operations'
    aws_creds_fp: str = f'{fs_root_path}{constants.aws_dir}/credentials'
    agent_registration_fp: str = f'{fs_root_path}{constants.agent_dir}/registration.json'
    agent_log_fp: str = f'{fs_root_path}{constants.install_log_dir}/local_cloud_agent.log'
    operation_log_fp: str = f'{operations_dir}/operations.log'
    update_operation_fp: str = f'{operations_dir}/update.json'
    repo_service_fp: str = f"{'/'.join([repo_dir, constants.relative_service_file_path])}"
    installed_service_fn: str = f'{fs_root_path}{constants.service_fn}'



conf_path = os.environ.get('LOCAL_CLOUD_AGENT_CONF_PATH', '/etc/local_cloud_agent/agent_config.yml')
with open(conf_path, 'r') as conf_file:
    conf = yaml.safe_load(conf_file)


agent_config = AgentConfig(**conf)
