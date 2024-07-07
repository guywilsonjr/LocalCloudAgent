import json
import logging
import os
import traceback

import pytest

from click.testing import CliRunner, Result



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


@pytest.mark.usefixtures("root_fakefs", "fake_base_fs")
def test_main() -> None:
    runner = CliRunner()
    from common import constants

    from cli import main
    result: Result = runner.invoke(main.install, [])

    log_cli_result(result)
    assert result.exit_code == 0
    assert result.output == ''
    assert os.path.exists(constants.installed_service_conf_fp)
    assert os.path.exists(constants.venv_dir)

