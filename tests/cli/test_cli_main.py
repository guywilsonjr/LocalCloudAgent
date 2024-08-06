import json
import logging
import os
import subprocess
import traceback
from typing import Optional, NamedTuple
from typer.testing import CliRunner, Result


class SubprocessTestCase(NamedTuple):
    cmd: list[str]
    exp_output: Optional[str] = None


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


def assert_dir_exists(dir_path: str) -> None:
    assert os.path.exists(dir_path)


def assert_dir_not_exists(dir_path: str) -> None:
    assert not os.path.exists(dir_path)


def run_single_subprocess(test_case: SubprocessTestCase) -> None:
    logging.info(f"Using CMD: {test_case.cmd} ")
    actual_cmd = " ".join(test_case.cmd)
    logging.info(f'Running subprocess: {actual_cmd}')
    sub_proc_res = subprocess.run(test_case.cmd, text=True, capture_output=True)
    logging.info(f'{actual_cmd}\nReturn Code: {sub_proc_res.returncode}\nStdout:\n{sub_proc_res.stdout}')
    assert sub_proc_res.returncode == 0
    if test_case.exp_output is not None:
        assert sub_proc_res.stdout == test_case.exp_output


# noinspection PyStatementEffect
def test_main() -> None:
    from local_cloud_agent.common.configuration import agent_config
    from local_cloud_agent.common import constants
    exp_dirs = [agent_config.metadata_dir, agent_config.conf_dir, agent_config.log_dir, agent_config.installed_service_fp, constants.systemd_conf_symlink_fp]
    logging.info(f'Expected directories: {exp_dirs}')

    [i for i in map(lambda x: assert_dir_not_exists(x), exp_dirs)]

    runner = CliRunner()
    from local_cloud_agent.cli import main
    cli_result: Result = runner.invoke(main.app, ['install'])
    log_cli_result(cli_result)
    assert cli_result.exit_code == 0

    [i for i in map(lambda x: assert_dir_exists(x), exp_dirs)]
    list_case = SubprocessTestCase(
        ['systemctl', 'list-unit-files', constants.installed_service_conf_fn],
        'UNIT FILE                 STATE   PRESET\nlocal_cloud_agent.service enabled enabled\n\n1 unit files listed.\n'
    )
    run_single_subprocess(list_case)

