import os
import string
import random

import pytest
from tests.test_common.test_fixtures import setup_file_system


@pytest.mark.asyncio
async def test_file_ops(setup_file_system):
    from local_cloud_agent.agent.configuration import agent_config
    test_fp = f'{agent_config.fs_root_path}/test.txt'
    from local_cloud_agent.agent import util
    first_char = random.choice(string.ascii_letters)
    second_char = random.choice(string.ascii_letters)
    await util.append_data_to_file(test_fp, first_char)
    first_read = await util.fetch_file_data(test_fp)
    assert first_read == first_char
    await util.append_data_to_file(test_fp, second_char)
    second_read = await util.fetch_file_data(test_fp)
    assert second_read == first_char + second_char

    await util.write_data_to_file(test_fp, first_char)
    third_read = await util.fetch_file_data(test_fp)
    assert third_read == first_char
    os.remove(test_fp)

