capital_keyword = 'LocalCloudAgent'
lower_keyword = 'local_cloud_agent'
repo_url = f'https://github.com/guywilsonjr/{capital_keyword}.git'
service_fn = f'{lower_keyword}.service'
repo_service_fp = f'src/{lower_keyword}/{service_fn}'
repo_conf_path = 'conf/agent_config.yml'
service_fn = f'/etc/systemd/system/{lower_keyword}.service'
repo_install_parent_dir = '/usr/local/src'
repo_dir = f'{repo_install_parent_dir}/{capital_keyword}'
venv_dir = f'/usr/local/{lower_keyword}/.venv'
root_dir = '/root'
metadata_dir = f'/var/local/{lower_keyword}'
install_conf_dir = f'/etc/{lower_keyword}'
install_conf_fn = 'agent_config.yml'
install_conf_fp = f'{install_conf_dir}/{install_conf_fn}'
install_log_dir = f'/var/log/{lower_keyword}'
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