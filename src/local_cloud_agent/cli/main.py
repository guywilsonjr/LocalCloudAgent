import os
import shutil
import subprocess
import venv

import git
import click

from common.configuration import agent_config
from common import constants, systemd


@click.group()
def main():
    return


@main.command()
def install():
    os.chdir(constants.repo_install_parent_dir)
    shutil.rmtree('/'.join([constants.repo_install_parent_dir, 'LocalCloudAgent']))
    git.Repo.clone_from(constants.repo_url, 'LocalCloudAgent', multi_options=['--depth', '1'])
    os.makedirs(constants.metadata_dir, exist_ok=True)
    os.makedirs(constants.install_conf_dir, exist_ok=True)
    os.makedirs(constants.install_log_dir, exist_ok=True)
    repo_service_conf_path = '/'.join([agent_config.repo_dir, constants.repo_service_fp])
    repo_agent_conf_path = '/'.join([agent_config.repo_dir, constants.repo_conf_path])
    shutil.copyfile(repo_service_conf_path, constants.service_fn)
    shutil.copyfile(repo_agent_conf_path, constants.repo_conf_path)
    venv.create(
        env_dir=constants.venv_dir,
        system_site_packages=False,
        with_pip=True,
        upgrade_deps=True
    )
    subprocess.run(['.venv/bin/pip', 'install', '-r', '/'.join([agent_config.repo_dir, 'requirements.txt'])])
    systemd.reload_systemd()


@main.command()
def uninstall():
    os.chdir(constants.repo_install_parent_dir)
    shutil.rmtree('/'.join([constants.repo_install_parent_dir, 'LocalCloudAgent']))
    '''''
    # If --purge
    os.remove(constants.metadata_dir)
    shutil.rmtree(constants.install_conf_dir)
    shutil.rmtree(constants.install_log_dir)
    os.remove(constants.service_fn)
    '''


if __name__ == '__main__':
    main()
