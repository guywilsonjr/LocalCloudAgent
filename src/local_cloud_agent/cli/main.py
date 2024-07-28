import logging
import os
import click

from common.configuration import agent_config
from common import constants, systemd
from app import app


def install_service() -> None:
    fp = agent_config.installed_service_fp

    with open(fp, 'w') as f:
        f.write(constants.service_file_data)
    logging.info('Service Installed Successfully')


@app.callback()
def main() -> None:
    if os.geteuid() != 0:
        raise RuntimeError('Must be run as root')
    else:
        print('Running as root user')


@main.command()
def install() -> None:
    logging.info('Creating metadata, configuration, and log directories')
    os.makedirs(agent_config.metadata_dir, exist_ok=True)
    os.makedirs(agent_config.conf_dir, exist_ok=True)
    os.makedirs(agent_config.log_dir, exist_ok=True)
    logging.info('Metadata, configuration, and log directories created')
    logging.info('Installing services')
    install_service()
    logging.info('Service Installed')
    systemd.reload_systemd()
    logging.info('Systemd reloaded sucessfully')


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
