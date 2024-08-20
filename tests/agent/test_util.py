import os
import string
import random

import pytest


@pytest.mark.asyncio
async def test_util() -> None:
    test_fp = f'test.txt'
    from local_cloud_agent.agent import util
    first_char = random.choice(string.ascii_letters)
    second_char = random.choice(string.ascii_letters)

    # Test Append and Fetch
    await util.append_data_to_file(test_fp, first_char)
    first_read = await util.fetch_file_data(test_fp)
    assert first_read == first_char
    await util.append_data_to_file(test_fp, second_char)
    second_read = await util.fetch_file_data(test_fp)
    assert second_read == first_char + second_char

    # Test Write and Fetch
    await util.write_data_to_file(test_fp, first_char)
    third_read = await util.fetch_file_data(test_fp)
    assert third_read == first_char
    os.remove(test_fp)

