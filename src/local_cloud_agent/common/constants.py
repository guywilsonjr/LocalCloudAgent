import os


capital_keyword = 'LocalCloudAgent'
lower_keyword = 'local_cloud_agent'
python_package_name = lower_keyword.replace('_', '-')
installed_service_conf_fn = f'{lower_keyword}.service'
etc_dir = '/etc'

installed_service_conf_dir = f'/usr/lib/systemd/system'
root_home_dir = '/root'
parent_metadata_dir = '/var/local'
metadata_dir = f'{parent_metadata_dir}/{lower_keyword}'
install_agent_conf_dir = f'{etc_dir}/{lower_keyword}'
var_log_dir = '/var/log'

install_log_dir = f'{var_log_dir}/{lower_keyword}'
systemd_conf_symlinkdir = '/etc/systemd/system/multi-user.target.wants'
systemd_conf_symlink_fp = f'{systemd_conf_symlinkdir}/{installed_service_conf_fn}'
'/usr/lib/systemd/system/test_startup.service'
aws_dir = f'{root_home_dir}/.aws'
aws_creds_fp = f'{aws_dir}/credentials'
agent_dir = f'{metadata_dir}/agent'
prefix_env_var = 'LOCAL_CLOUD_AGENT_PREFIX'
# TODO REMOVE FILE AND FILE USAGES AND REPLACE WITH CREATED FILE BELOW
service_file_data = f"""[Unit]
Description=Local Cloud Agent
After=network.target

[Service]
ExecStart={os.environ['VIRTUAL_ENV']}/bin/python3 ERROR/main.py
Restart=always
"""
service_file_data = """[Unit]
Description=Sample Script Startup

[Service]
Type=idle
ExecStart=/bin/echo "hello world"
"""

root_debug_msg = 'Running as root user'

