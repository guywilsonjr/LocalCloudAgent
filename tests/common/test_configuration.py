import os
import shutil


from local_cloud_agent.common.configuration import ensure_dirs_exist, validate_fs, agent_config


def test_ensure_dirs_exist():
    if os.path.exists(agent_config.metadata_dir):
        shutil.rmtree(agent_config.metadata_dir)
    assert not os.path.exists(agent_config.metadata_dir)
    ensure_dirs_exist()
    assert os.path.exists(agent_config.metadata_dir)
    assert os.path.exists(agent_config.agent_dir)
    assert os.path.exists(agent_config.operations_dir)


def test_validate_fs():
    os.makedirs('/root/.aws', exist_ok=True)
    with open('/root/.aws/credentials', 'w') as f:
        f.write('')
    validate_fs()

    os.remove('/root/.aws/credentials')
    shutil.rmtree('/root')


