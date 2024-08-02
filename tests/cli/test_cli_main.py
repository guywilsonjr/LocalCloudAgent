import json
import logging
import os
import traceback

from typer.testing import CliRunner, Result


def log_cli_result(result: Result) -> None:
    err_type, err, tb = result.exc_info
    logging.info(
        json.dumps({
            'Output': result.output,
            'Exit Code': result.exit_code,
            'Error Type': str(err_type),
            'Error': str(err),
            'Traceback': traceback.format_tb(tb),
            'Exception': str(result.exception),
            'Return Value': result.return_value
        }, indent=2)
    )


def assert_dir_exists(dir: str) -> None:
    assert os.path.exists(dir)


def test_main() -> None:
    runner = CliRunner()
    from cli import main
    result: Result = runner.invoke(main.app, ['install'])

    log_cli_result(result)
    assert result.exit_code == 0
    from common.configuration import agent_config
    exp_dirs = [agent_config.metadata_dir, agent_config.conf_dir, agent_config.log_dir, agent_config.installed_service_fp]

    # noinspection PyStatementEffect
    [i for i in map(lambda x: assert_dir_exists(x), exp_dirs)]

