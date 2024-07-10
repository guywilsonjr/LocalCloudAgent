import json
import logging
import os
import traceback

import pystemd
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


def test_main(monkeypatch) -> None:
    runner = CliRunner()
    with runner.isolated_filesystem('/tmp') as tmpdir:
        with monkeypatch.context() as m:
            m.setattr('common.systemd.reload_systemd', lambda: None)
            m.setenv('LOCAL_CLOUD_AGENT_PREFIX', tmpdir)
            m.setattr(os, 'geteuid', lambda: 0)
            logging.info(f'Using Isolated filesystem: {tmpdir}')
            from cli import main
            result: Result = runner.invoke(main.main, ['install'])

            log_cli_result(result)
            assert result.exit_code == 0
            assert result.output == ''
