import os


home_dir = '/root'
log_dir = '/var/log/local_cloud_agent'

local_cloud_agent_dir = f'{home_dir}/.local_cloud_agent'
agent_dir = f'{local_cloud_agent_dir}/agent'
operations_dir = f'{local_cloud_agent_dir}/operations'
repo_dir = '/usr/local/LocalCloudAgent'
aws_dir = f'{home_dir}/.aws'
aws_creds_fp = f'{aws_dir}/credentials'

agent_registration_fp = f'{agent_dir}/registration.json'
agent_log_fp = f'{log_dir}/agent.log'
operation_log_fp = f'{local_cloud_agent_dir}/operations/operations.log'
update_operation_fp = f'{local_cloud_agent_dir}/operations/update.json'
latest_running_version_fp = f'{local_cloud_agent_dir}/latest_running_version'
repo_url = 'https://github.com/guywilsonjr/LocalCloudAgent'
