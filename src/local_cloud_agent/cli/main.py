import logging
import os

from local_cloud_agent.common.configuration import agent_config

from local_cloud_agent.common import constants, err_constants
import typer

# TODO: Use typer
app = typer.Typer()


def install_service() -> None:
    fp = agent_config.installed_service_fp

    with open(fp, 'w') as f:
        f.write(constants.service_file_data)
    logging.info('Service Installed Successfully')


def root_check() -> None:
    if os.geteuid() != 0:
        raise RuntimeError(err_constants.root_err_msg)
    else:
        typer.echo(constants.root_debug_msg)


@app.callback(invoke_without_command=True)
def main() -> None:
    root_check()


@app.command()
def install() -> None:
    print('Creating metadata, configuration, and log directories')
    os.makedirs(agent_config.metadata_dir, exist_ok=True)
    os.makedirs(agent_config.conf_dir, exist_ok=True)
    os.makedirs(agent_config.log_dir, exist_ok=True)
    print('Metadata, configuration, and log directories created')
    print('Installing services')
    install_service()
    print('Service Installed')
    # TODO
    print('Systemd reloaded sucessfully')


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


if __name__ == '__main__':
    app()
