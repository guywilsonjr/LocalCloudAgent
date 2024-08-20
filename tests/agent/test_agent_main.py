import importlib
import runpy
from contextlib import asynccontextmanager

import aioboto3
import pytest
import pytest_mock
import types_aiobotocore_sqs.client
from types_aiobotocore_sqs.client import SQSClient

from tests.common_test import eval_constants
from tests.common_test.eval_constants import test_agent_shell_op, test_agent_state
from local_cloud_agent.agent.models import AgentOperationResult
from local_cloud_agent.agent.operations.update import shell_command
from tests.common_test import mocks


class MockSQSClient:
    def __init__(self, *args, **kwargs) -> None:
        pass

    async def delete_message(self, *args, **kwargs) -> None:
        return None

    async def receive_message(self, *args, **kwargs) -> dict[str, None]:
        return {'Messages': None}


@pytest.mark.asyncio
@pytest.mark.usefixtures("registered_agent")
async def test_main_execute_operation(mocker: pytest_mock.plugin.MockerFixture) -> None:
    from local_cloud_agent.agent.operations.update import shell_command
    from local_cloud_agent.agent import main

    resp = mocks.MockAIOHttpResponse()
    mocker.patch('aiohttp.ClientSession.patch', return_value=resp)
    await main.execute_operation(
        agent_state=test_agent_state,
        operation_func=shell_command,
        operation=test_agent_shell_op
    )


    await main.execute_operation(
        agent_state=test_agent_state,
        operation_func=eval_constants.test_async_exception,
        operation=test_agent_shell_op
    )
    await main.execute_operation(
        agent_state=test_agent_state,
        operation_func=eval_constants.test_op_with_post_op,
        operation=test_agent_shell_op
    )







@pytest.mark.asyncio
@pytest.mark.usefixtures("registered_agent")
async def test_receive_message() -> None:
    from local_cloud_agent.agent import main
    await main.get_sqs_response(MockSQSClient(), 'test_queue_url')
    resp = await main.receive_message(
        MockSQSClient(),
        'test_queue_url',
        operation=test_agent_shell_op,
        message={'ReceiptHandle': 'test'}
    )
    assert resp == shell_command



@pytest.mark.asyncio
@pytest.mark.usefixtures("registered_agent")
async def test_poll_queue(mocker: pytest_mock.plugin.MockerFixture) -> None:
    from local_cloud_agent.agent import main
    mocker.patch('local_cloud_agent.agent.main.get_sqs_response', return_value={'Messages': None})

    await main.poll_queue(test_agent_state, MockSQSClient(), 'test_queue_url')
    mocker.patch(
        'local_cloud_agent.agent.main.get_sqs_response',
        return_value={
            'Messages': [{'Body': test_agent_shell_op.operation.model_dump_json(), 'ReceiptHandle': 'test'}]
        })
    resp = mocks.MockAIOHttpResponse()
    mocker.patch('aiohttp.ClientSession.patch', return_value=resp)
    await main.poll_queue(test_agent_state, MockSQSClient(), 'test_queue_url')


@pytest.mark.asyncio
@pytest.mark.usefixtures("registered_agent")
async def test_listen_to_queue(mocker: pytest_mock.plugin.MockerFixture) -> None:
    from local_cloud_agent.agent import main
    mocker.patch('asyncio.sleep', eval_constants.test_async_exception)

    @asynccontextmanager
    async def get_mock_client(*args, **kwargs) -> MockSQSClient:
        yield MockSQSClient()
    mocker.patch('aioboto3.Session.client', get_mock_client)

    with pytest.raises(Exception):
        await main.listen_to_queue(eval_constants.test_agent_state)


@pytest.mark.asyncio
@pytest.mark.usefixtures("registered_agent")
async def test_async_main(mocker: pytest_mock.plugin.MockerFixture) -> None:
    from local_cloud_agent.agent import main
    mocker.patch('asyncio.sleep', eval_constants.test_async_exception)

    @asynccontextmanager
    async def get_mock_client(*args, **kwargs) -> MockSQSClient:
        yield MockSQSClient()

    mocker.patch('aioboto3.Session.client', get_mock_client)

    with pytest.raises(Exception):
        await main.async_main()



@pytest.mark.usefixtures("registered_agent")
def test_main(mocker: pytest_mock.plugin.MockerFixture) -> None:
    from local_cloud_agent.agent import main
    mocker.patch('asyncio.sleep', eval_constants.test_async_exception)

    @asynccontextmanager
    async def get_mock_client(*args, **kwargs) -> MockSQSClient:
        yield MockSQSClient()

    mocker.patch('aioboto3.Session.client', get_mock_client)

    with pytest.raises(Exception):
        main.main()

