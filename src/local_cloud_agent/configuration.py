# Must use minimal imports to avoid circular imports
import os
import yaml
from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    home_dir: str = Field(alias='HOME_DIR')
    log_dir: str = Field(alias='LOG_DIR')
    aws_dir: str = Field(alias='AWS_DIR')
    repo_dir: str = Field(alias='REPO_DIR')

    @property
    def local_cloud_agent_dir(self):
        return f'{self.home_dir}/.local_cloud_agent'

    @property
    def agent_dir(self):
        return f'{self.local_cloud_agent_dir}/agent'

    @property
    def operations_dir(self):
        return f'{self.local_cloud_agent_dir}/operations'

    @property
    def aws_creds_fp(self):
        return f'{self.aws_dir}/credentials'

    @property
    def agent_registration_fp(self):
        return f'{self.agent_dir}/registration.json'

    @property
    def agent_log_fp(self):
        return f'{self.log_dir}/agent.log'

    @property
    def operation_log_fp(self):
        return f'{self.operations_dir}/operations.log'

    @property
    def update_operation_fp(self):
        return f'{self.operations_dir}/update.json'


conf_path = os.environ.get('LOCAL_CLOUD_AGENT_CONF_PATH', '/etc/local_cloud_agent/agent_config.yml')
with open(conf_path, 'r') as conf_file:
    conf = yaml.safe_load(conf_file)


agent_config = AgentConfig(**conf)
repo_url = 'https://github.com/guywilsonjr/LocalCloudAgent'
