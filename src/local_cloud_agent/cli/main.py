import os
import shutil
import subprocess
import venv
import git
import click

from common.configuration import agent_config
from common import constants, systemd
import getpass




def install_service():
    with open(constants.installed_service_conf_fp, 'w') as f:
        f.write(constants.service_file_data)


@click.group()
def main():
    if os.geteuid() != 0:
        raise RuntimeError(getpass.getuser())


@main.command()
def install():
    os.chdir(constants.repo_install_parent_dir)
    shutil.rmtree('/'.join([constants.repo_install_parent_dir, 'LocalCloudAgent']))
    git.Repo.clone_from(constants.repo_url, 'LocalCloudAgent', multi_options=['--depth', '1'])
    os.makedirs(constants.metadata_dir, exist_ok=True)
    os.makedirs(constants.install_agent_conf_dir, exist_ok=True)
    os.makedirs(constants.install_log_dir, exist_ok=True)
    install_service()
    venv.create(
        env_dir=constants.venv_dir,
        system_site_packages=False,
        with_pip=True,
        upgrade_deps=True
    )
    subprocess.run(['.venv/bin/pip', 'install', '-r', f'{agent_config.repo_dir}/requirements.txt'])
    systemd.reload_systemd()


@main.command()
@click.option('--purge', is_flag=True)
def uninstall():
    os.chdir(constants.repo_install_parent_dir)
    shutil.rmtree(f'{constants.repo_install_parent_dir}/LocalCloudAgent')
    '''''
    # If --purge
    os.remove(constants.metadata_dir)
    shutil.rmtree(constants.install_conf_dir)
    shutil.rmtree(constants.install_log_dir)
    os.remove(constants.service_fn)
    '''


if __name__ == '__main__':
    main()
