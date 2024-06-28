capital_keyword = 'LocalCloudAgent'
lower_keyword = 'local_cloud_agent'
repo_url = f'https://github.com/guywilsonjr/{capital_keyword}.git'
relative_service_file_path = f'src/{lower_keyword}/local_cloud_agent.service'
relative_repo_conf_path = 'conf/agent_config.yml'
service_fn = f'/etc/systemd/system/{lower_keyword}.service'
repo_install_dir = '/usr/local'
repo_dir = f'{repo_install_dir}/{capital_keyword}'
venv_dir = f'{repo_dir}/.venv'
root_dir = '/root'
metadata_dir = f'{root_dir}/.{lower_keyword}'
install_conf_dir = f'/etc/{lower_keyword}'
install_log_dir = f'/var/log/{lower_keyword}'
installed_repo_dir = f'{repo_install_dir}/{capital_keyword}'
aws_dir = f'{root_dir}/.aws'
aws_creds_fp = f'{aws_dir}/credentials'
agent_dir = f'{metadata_dir}/agent'
