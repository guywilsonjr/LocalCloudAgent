import shutil
import os


if os.getlogin() != 'root':
    print('Please run this script as root.')
    exit(1)

shutil.copyfile('conf/local_cloud_agent.service', '/lib/systemd/system directory/local_cloud_agent.service')
shutil.copyfile('conf/agent_config.yml', '/etc/local_cloud_agent/agent_config.yml')
