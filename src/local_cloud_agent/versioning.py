from typing import Tuple

from cumulonimbus_models.operations import OperationResult, OperationResultStatus
from git import Git, Repo, TagReference

from configuration import repo_url, agent_config
from models import PersistedOperation
from util import logger, write_data_to_file


def get_latest_tag() -> TagReference:
    repo = Repo(agent_config.repo_dir)
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    latest_tag = tags[-1]
    return latest_tag


def get_base_tag_version(tag: TagReference) -> Tuple[int, int, int]:
    if '-' in tag.name:
        period_separated_vers = tag.name.split('-')[0][1:]
    else:
        period_separated_vers = tag.name[1:]
    return tuple(map(int, period_separated_vers.split('.')))


def get_release_candidate_version(tag: TagReference) -> int:
    if '-' in tag.name:
        return int(tag.name.split('-')[1][2:])
    else:
        return None


def get_latest_available_version() -> str:
    git_cmd = Git()
    resp = git_cmd.ls_remote(repo_url, sort='v:refname')
    resp_lines = resp.split('\n')
    valid_entries = [line for line in resp_lines if '{}' not in line and 'HEAD' not in line]
    latest_entry = valid_entries[-1]
    ref_entry = latest_entry.split('\t')[-1]
    version = ref_entry.split('/')[-1]
    return version


async def get_version() -> str:
    # Check if the version is set in the environment OF THE REPO DIR

    return ''


async def update_repository() -> None:
    repo = Repo(agent_config.repo_dir)
    remote = repo.remote()
    remote.pull()


async def update_repo_and_docker_image(operation: PersistedOperation) -> OperationResult:
    logger.info('Updating Repository and Docker Image')
    await write_data_to_file(agent_config.update_operation_fp, operation.model_dump_json())
    await update_repository()
    return OperationResult(
        operation_output='SUCCESS',
        operation_status=OperationResultStatus.SUCCESS
    )

