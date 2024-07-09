import pytest
from tests.common_test import test_constants

# TODO: create fixture with tmp_path/usr/local/src so that we can test the git_common install functions


@pytest.mark.usefixtures("usr_local_src")
def test_git_common():
    from common import git_common
    git_common.clone_repo(None)
    tag = git_common.get_latest_tag()
    assert tag == test_constants.test_version

    major, minor, patch = git_common.get_base_tag_version(tag)
    assert major == test_constants.test_major_version
    assert minor == test_constants.test_minor_version
    assert patch == test_constants.test_patch_version

    rc = git_common.get_release_candidate_version(tag)
    assert rc == test_constants.test_rc_version
    latest_available_version = git_common.get_latest_available_version()
    assert latest_available_version == test_constants.test_version
    version_info = git_common.get_version_info(tag)
    assert version_info == test_constants.test_version_info

