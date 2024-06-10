import os
from git import Git

from constants import repo_url
from util import logger


def get_latest_available_version() -> str:
    git_cmd = Git()
    resp = git_cmd.ls_remote(repo_url, sort='v:refname')
    resp_lines = resp.split('\n')
    valid_entries = [line for line in resp_lines if '{}' not in line and 'HEAD' not in line]
    latest_entry = valid_entries[-1]
    ref_entry = latest_entry.split('\t')[-1]
    version = ref_entry.split('/')[-1]
    return version




async def startup():
    version = os.environ['VERSION']
    logger.info(os.environ)
    logger.info(f'Starting Local Cloud Agent version: {version}')
