import json
import logging
import os
import pytest

from click.testing import CliRunner, Result

from common import constants


def log_cli_result(result: Result) -> None:
    logging.info(
        json.dumps({
            'Output': result.output,
            'Exc Info': str(result.exc_info),
            'Exception': str(result.exception),
            'Return Value': result.return_value
        }, indent=2)
    )


@pytest.mark.usefixtures("root_fakefs", "fake_base_fs")
def test_main() -> None:
    from cli import main
    runner = CliRunner()
    result: Result = runner.invoke(main.install, [])

    log_cli_result(result)
    assert result.exit_code == 0
    assert result.output == ''
    assert os.path.exists(constants.installed_service_conf_fp)
    assert os.path.exists(constants.venv_dir)
    assert os.path.exists(constants.repo_python_path)

