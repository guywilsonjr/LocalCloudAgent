import logging
from typing import cast, List, Optional, Tuple, TypedDict
import re
import pygit2
from agent.models import VersionInfo
from common import constants
from common.configuration import agent_config


def clone_repo() -> pygit2.Repository:
    logging.info(f'Cloning repository to {agent_config.repo_dir}')
    repo = pygit2.clone_repository(constants.repo_url, agent_config.repo_dir)
    logging.info(f'Cloned repository to {agent_config.repo_dir}')
    latest_version = get_latest_available_version()
    repo.checkout(f'refs/tags/{latest_version}')
    return repo


def get_version() -> str:
    logging.info(f'Getting latest tag from repo: {agent_config.repo_dir}')
    repo = pygit2.Repository(agent_config.repo_dir)
    regex = re.compile('^refs/tags/')
    return [r for r in cast(List[str], repo.references) if regex.match(r)][-1].split('/')[-1]



def get_base_tag_version(tag: str) -> Tuple[int, int, int]:
    if '-' in tag:
        period_separated_vers = tag.split('-')[0][1:]
    else:
        period_separated_vers = tag[1:]
    major, minor, patch = tuple(map(int, period_separated_vers.split('.')))
    return major, minor, patch


def get_release_candidate_version(tag: str) -> Optional[int]:
    if '-' in tag:
        return int(tag.split('-')[1][2:])
    else:
        return None


def get_version_info(tag: str) -> VersionInfo:
    major, minor, patch = get_base_tag_version(tag)
    rc = get_release_candidate_version(tag)
    return VersionInfo(major=major, minor=minor, patch=patch, release_candidate=rc)


class TagRef(TypedDict):
    name: str


def get_latest_available_version() -> str:
    repo = pygit2.Repository(agent_config.repo_dir)
    remote_origin = repo.remotes["origin"]
    ls_remotes = remote_origin.ls_remotes()
    tags = [
        ref for ref in cast(List[TagRef], ls_remotes)
        if 'refs/tags' in ref['name'] and '^{}' not in ref['name']
    ]
    if tags[-1]['name']:
        latest_tag = tags[-1]['name'].split('/')[-1]
        return latest_tag
    else:
        raise RuntimeError(f'Invalid tags found for repository at: {agent_config.repo_dir}')


