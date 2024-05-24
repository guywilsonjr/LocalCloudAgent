import os

from constants import agent_dir, aws_creds_fp, home_dir, local_cloud_agent_dir, operations_dir, repo_dir


os.makedirs(local_cloud_agent_dir, exist_ok=True)
os.makedirs(agent_dir, exist_ok=True)
os.makedirs(operations_dir, exist_ok=True)

if not os.path.exists(repo_dir):
    raise RuntimeError(f'Repo dir not found: {repo_dir}')

if not os.path.exists(aws_creds_fp):
    home_list = os.listdir(home_dir)
    base_msg = 'AWS credentials not found. Please run `aws configure` to set up your credentials.'
    home_msg = f'Home Dir: {home_dir}, Files: {home_list}'
    msg = '\n'.join([base_msg, home_msg])
    raise RuntimeError(msg)
