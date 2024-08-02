import os


capital_keyword = 'LocalCloudAgent'
lower_keyword = 'local_cloud_agent'
installed_service_conf_fp = f'{lower_keyword}.service'
parent_conf_dir = '/etc'
installed_service_conf_dir = f'{parent_conf_dir}/systemd/system'
root_home_dir = '/root'
parent_metadata_dir = '/var/local'
metadata_dir = f'{parent_metadata_dir}/{lower_keyword}'
install_agent_conf_dir = f'{parent_conf_dir}/{lower_keyword}'
parent_log_dir = '/var/log'
install_log_dir = f'{parent_log_dir}/{lower_keyword}'
aws_dir = f'{root_home_dir}/.aws'
aws_creds_fp = f'{aws_dir}/credentials'
agent_dir = f'{metadata_dir}/agent'
var_local_dir = '/var/local'
var_log_dir = '/var/log'
etc_dir = '/etc'
prefix_env_var = 'LOCAL_CLOUD_AGENT_PREFIX'
# TODO REMOVE FILE AND FILE USAGES AND REPLACE WITH CREATED FILE BELOW
service_file_data = f"""[Unit]
Description=Local Cloud Agent
After=network.target

[Service]
ExecStart={os.environ['VIRTUAL_ENV']}/bin/python3 ERROR/main.py
Restart=always
"""

root_debug_msg = 'Running as root user'

