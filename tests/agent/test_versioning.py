import pytest
from tests.test_common.test_fixtures import setup_file_system, test_major_version, test_minor_version, test_patch_version, test_rc_version, test_version, test_version_info


@pytest.mark.asyncio
async def test_versioning(setup_file_system):
    import agent.versioning
    tag = agent.versioning.get_latest_tag()
    assert tag.name == test_version

    major, minor, patch = agent.versioning.get_base_tag_version(tag)
    assert major == test_major_version
    assert minor == test_minor_version
    assert patch == test_patch_version

    rc = agent.versioning.get_release_candidate_version(tag)
    assert rc == test_rc_version
    latest_available_version = agent.versioning.get_latest_available_version()
    assert latest_available_version == test_version
    version_info = agent.versioning.get_version_info(tag)
    assert version_info == test_version_info

