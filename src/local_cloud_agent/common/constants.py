capital_keyword = 'LocalCloudAgent'
lower_keyword = 'local_cloud_agent'
repo_url = f'https://github.com/guywilsonjr/{capital_keyword}.git'
installed_service_conf_fp = f'{lower_keyword}.service'
relative_repo_service_fp = f'src/{lower_keyword}/{installed_service_conf_fp}'
parent_conf_dir = '/etc'
installed_service_conf_dir = f'{parent_conf_dir}/systemd/system'
installed_service_conf_fp = f'{installed_service_conf_dir}/{lower_keyword}.service'
system_usr_local_dir = '/usr/local'
repo_install_parent_dir = f'{system_usr_local_dir}/src'
repo_dir = f'{repo_install_parent_dir}/{capital_keyword}'
venv_parent_dir = f'{system_usr_local_dir}/{lower_keyword}'
venv_dir = f'{venv_parent_dir}/.venv'
root_dir = '/root'
parent_metadata_dir = '/var/local'
metadata_dir = f'{parent_metadata_dir}/{lower_keyword}'
install_agent_conf_dir = f'{parent_conf_dir}/{lower_keyword}'
agent_conf_fn = 'agent_config.yml'
installed_agent_conf_fp = f'{install_agent_conf_dir}/{agent_conf_fn}'
parent_log_dir = '/var/log'
install_log_dir = f'{parent_log_dir}/{lower_keyword}'
installed_repo_dir = f'{repo_install_parent_dir}/{capital_keyword}'
aws_dir = f'{root_dir}/.aws'
aws_creds_fp = f'{aws_dir}/credentials'
agent_dir = f'{metadata_dir}/agent'
repo_python_path = f'{installed_repo_dir}/src/{lower_keyword}'

# TODO REMOVE FILE AND FILE USAGES AND REPLACE WITH CREATED FILE BELOW
service_file_data = f'''[Unit]
Description=Local Cloud Agent
After=network.target

[Service]
ExecStart={venv_dir}/bin/python3 {repo_python_path}/main.py
Restart=always
Environment="PYTHONPATH={repo_python_path}"
'''