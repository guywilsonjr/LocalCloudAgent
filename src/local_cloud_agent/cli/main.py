import logging
import os
import shutil
import subprocess
import venv
import click

from common.configuration import agent_config
from common import constants, git_common, systemd




def install_service() -> None:
    fp = agent_config.installed_service_fp
    with open(fp, 'w') as f:
        f.write(constants.service_file_data)
    logging.info('Service Installed Successfully')


@click.group()
def main() -> None:
    if os.geteuid() != 0:
        raise RuntimeError('Must be run as root')


@main.command()
def install() -> None:
    starting_dir = os.getcwd()
    logging.info(f'Installing repository')
    if os.path.exists(agent_config.repo_dir):
        logging.info('Removing existing installation')
        shutil.rmtree(agent_config.repo_dir)
    os.makedirs(agent_config.repo_parent_dir, exist_ok=True)
    git_common.clone_repo()
    logging.info('Repository Installed')
    logging.info('Creating metadata, configuration, and log directories')
    os.makedirs(agent_config.metadata_dir, exist_ok=True)
    os.makedirs(agent_config.conf_dir, exist_ok=True)
    os.makedirs(agent_config.log_dir, exist_ok=True)
    logging.info('Metadata, configuration, and log directories created')
    logging.info('Installing services')
    install_service()
    logging.info('Service Installed')
    logging.info('Creating Virtual environment')
    venv.create(
        env_dir=agent_config.venv_dir,
        system_site_packages=False,
        with_pip=True,
        upgrade_deps=True
    )
    logging.info('Virtual Environment Created')
    os.chdir(agent_config.venv_parent_dir)
    logging.info('Installing pip dependencies')
    subprocess.run([f'{agent_config.venv_dir}/bin/pip', 'install', '-r', f'{agent_config.repo_dir}/requirements.txt'])
    logging.info('Pip dependencies installed')
    logging.info('Reloading Systemd')
    systemd.reload_systemd()
    logging.info('Systemd reloaded sucessfully')
    os.chdir(starting_dir)


@main.command()
@click.option('--purge', is_flag=True)
def uninstall() -> None:
    pass
    '''''
    # If --purge
    os.remove(constants.metadata_dir)
    shutil.rmtree(constants.install_conf_dir)
    shutil.rmtree(constants.install_log_dir)
    os.remove(constants.service_fn)
    '''


if __name__ == '__main__':
    main()
