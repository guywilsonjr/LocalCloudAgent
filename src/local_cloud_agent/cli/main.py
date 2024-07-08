import logging
import os
import shutil
import subprocess
import venv
import click

from common.configuration import agent_config
from common import configuration
from common import constants, git_common, systemd




def install_service():
    fp = configuration.get_prefixed_dir(constants.installed_service_conf_fp)
    with open(fp, 'w') as f:
        f.write(constants.service_file_data)
    logging.info('Service Installed Successfully')


@click.group()
def main():
    if os.geteuid() != 0:
        raise RuntimeError('Must be run as root')


@main.command()
def install():
    starting_dir = os.getcwd()
    logging.info(f'Installing repository')
    if os.path.exists(configuration.get_prefixed_dir(constants.installed_repo_dir)):
        logging.info('Removing existing installation')
        shutil.rmtree(configuration.get_prefixed_dir(constants.installed_repo_dir))
    os.makedirs(configuration.get_prefixed_dir(constants.repo_install_parent_dir))
    logging.info(f'Cloning repository into directory: {configuration.get_prefixed_dir(constants.installed_repo_dir)}')
    git_common.clone_repo(constants.repo_url, configuration.get_prefixed_dir(constants.installed_repo_dir))
    logging.info('Repository Installed')
    logging.info('Creating metadata, configuration, and log directories')
    os.makedirs(configuration.get_prefixed_dir(constants.metadata_dir), exist_ok=True)
    os.makedirs(configuration.get_prefixed_dir(constants.install_agent_conf_dir), exist_ok=True)
    os.makedirs(configuration.get_prefixed_dir(constants.install_log_dir), exist_ok=True)
    logging.info('Metadata, configuration, and log directories created')
    logging.info('Installing services')
    install_service()
    logging.info('Service Installed')
    logging.info('Creating Virtual environment')
    venv.create(
        env_dir=configuration.get_prefixed_dir(constants.venv_dir),
        system_site_packages=False,
        with_pip=True,
        upgrade_deps=True
    )
    logging.info('Virtual Environment Created')
    os.chdir(configuration.get_prefixed_dir(constants.venv_parent_dir))
    logging.info('Installing pip dependencies')
    subprocess.run([f'{configuration.get_prefixed_dir(constants.venv_dir)}/bin/pip', 'install', '-r', f'{agent_config.repo_dir}/requirements.txt'])
    logging.info('Pip dependencies installed')
    logging.info('Reloading Systemd')
    systemd.reload_systemd()
    logging.info('Systemd reloaded sucessfully')
    os.chdir(starting_dir)


@main.command()
@click.option('--purge', is_flag=True)
def uninstall():
    os.chdir(configuration.get_prefixed_dir(constants.repo_install_parent_dir))
    shutil.rmtree(configuration.get_prefixed_dir(f'{constants.repo_install_parent_dir}/LocalCloudAgent'))
    '''''
    # If --purge
    os.remove(constants.metadata_dir)
    shutil.rmtree(constants.install_conf_dir)
    shutil.rmtree(constants.install_log_dir)
    os.remove(constants.service_fn)
    '''


if __name__ == '__main__':
    main()
