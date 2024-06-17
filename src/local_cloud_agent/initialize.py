import os

from configuration import agent_config


def ensure_dirs_exist():
    os.makedirs(agent_config.local_cloud_agent_dir, exist_ok=True)
    os.makedirs(agent_config.agent_dir, exist_ok=True)
    os.makedirs(agent_config.operations_dir, exist_ok=True)


def validate_fs():
    ensure_dirs_exist()
    if not os.path.exists(agent_config.repo_dir):
        raise RuntimeError(f'Repo dir not found: {agent_config.repo_dir}')

    if not os.path.exists(agent_config.aws_creds_fp):
        home_list = os.listdir(agent_config.home_dir)
        base_msg = 'AWS credentials not found. Please run `aws configure` to set up your credentials.'
        home_msg = f'Home Dir: {agent_config.home_dir}, Files: {home_list}'
        msg = '\n'.join([base_msg, home_msg])
        raise RuntimeError(msg)

