from typing import Tuple

from git import Git, Repo, TagReference

from agent.models import VersionInfo
from agent.post_config import logger
from common import constants
from common.configuration import agent_config


def get_latest_tag() -> TagReference:
    logger.info(f'Getting latest tag from repo: {agent_config.repo_dir}')
    repo = Repo(agent_config.repo_dir)
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    latest_tag = tags[-1]
    return latest_tag


def get_base_tag_version(tag: TagReference) -> Tuple[int, int, int]:
    if '-' in tag.name:
        period_separated_vers = tag.name.split('-')[0][1:]
    else:
        period_separated_vers = tag.name[1:]
    major, minor, patch = tuple(map(int, period_separated_vers.split('.')))
    return major, minor, patch


def get_release_candidate_version(tag: TagReference) -> int:
    if '-' in tag.name:
        return int(tag.name.split('-')[1][2:])
    else:
        return None


def get_version_info(tag: TagReference) -> VersionInfo:
    major, minor, patch = get_base_tag_version(tag)
    rc = get_release_candidate_version(tag)
    return VersionInfo(major=major, minor=minor, patch=patch, release_candidate=rc)


def get_latest_available_version() -> str:
    git_cmd = Git()
    resp = git_cmd.ls_remote(constants.repo_url, sort='v:refname')
    resp_lines = resp.split('\n')
    valid_entries = [line for line in resp_lines if '{}' not in line and 'HEAD' not in line]
    latest_entry = valid_entries[-1]
    ref_entry = latest_entry.split('\t')[-1]
    version = ref_entry.split('/')[-1]
    return version



