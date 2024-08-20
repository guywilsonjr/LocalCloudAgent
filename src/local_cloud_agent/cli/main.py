import importlib
import logging
import os
import pathlib
import typer

from local_cloud_agent.common.configuration import agent_config
from local_cloud_agent.common import constants, err_constants


app = typer.Typer()


def install_service() -> None:
    print('Installing services')
    fp_location = str(importlib.resources.files('local_cloud_agent').joinpath('conf/local_cloud_agent.service'))
    pathlib.Path(agent_config.installed_service_fp).unlink(missing_ok=True)
    logging.info(f'Creating symlink from {fp_location} to {agent_config.installed_service_fp}')
    os.symlink(fp_location, agent_config.installed_service_fp)
    pathlib.Path(constants.systemd_conf_symlink_fp).unlink(missing_ok=True)
    logging.info(f'Creating symlink from {agent_config.installed_service_fp} to {constants.systemd_conf_symlink_fp}')
    os.symlink(agent_config.installed_service_fp, constants.systemd_conf_symlink_fp)
    print('Service Installed Successfully')


def root_check() -> None:
    if os.geteuid() != 0:
        raise RuntimeError(err_constants.root_err_msg)
    else:
        typer.echo(constants.root_debug_msg)


@app.callback(invoke_without_command=True)
def main() -> None:
    root_check()


# TODO: RELOAD AFTER INSTALL
@app.command()
def install() -> None:
    print('Creating metadata, configuration, and log directories')
    os.makedirs(agent_config.metadata_dir, exist_ok=True)
    os.makedirs(agent_config.agent_dir, exist_ok=True)
    os.makedirs(agent_config.operations_dir, exist_ok=True)
    os.makedirs(agent_config.conf_dir, exist_ok=True)
    os.makedirs(agent_config.log_dir, exist_ok=True)
    print('Metadata, configuration, and log directories created')
    install_service()
    # TODO: RELOAD SYSTEMD
    print('Systemd reloaded sucessfully')


if __name__ == '__main__': # pragma: no cover
    app()


'''
@app.command()
#@click.option('--purge', is_flag=True)
def uninstall() -> None:
    pass
    """''
    # If --purge
    os.remove(constants.metadata_dir)
    shutil.rmtree(constants.install_conf_dir)
    shutil.rmtree(constants.install_log_dir)
    os.remove(constants.service_fn)
    """
'''

