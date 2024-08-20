from contextlib import asynccontextmanager

import pytest
import pytest_mock
from cumulonimbus_models.agent import AgentRegisterResponse

from local_cloud_agent.agent.models import AgentState
from tests.common_test import eval_constants


@pytest.mark.usefixtures("registered_agent")
@pytest.mark.asyncio
async def test_register_agent_request(mocker: pytest_mock.plugin.MockerFixture) -> None:
    from local_cloud_agent.agent import agent_info
    resp = await agent_info.get_registration()
    assert resp == AgentRegisterResponse(
        agent_id=eval_constants.test_agent_id,
        agent_key=eval_constants.test_agent_key,
        ip_address=eval_constants.test_ip_address,
        operations_queue_url=eval_constants.test_operations_queue_url
    )


    class TestObj:
        async def json(self) -> dict:
            return eval_constants.test_register_agent_response.model_dump()

        status = 200
        _text = eval_constants.test_register_agent_response.model_dump_json()

        async def text(self) -> str:
            return self._text

    @asynccontextmanager
    async def get_400_test_obj() -> TestObj:
        test_obj = TestObj()
        test_obj.status = 400
        test_obj._text = 'test_error'
        yield test_obj

    @asynccontextmanager
    async def get_200_test_obj() -> TestObj:
        yield TestObj()



    mocker.patch('aiohttp.ClientSession.post', return_value=get_200_test_obj())
    resp = await agent_info.register_agent_request(eval_constants.test_register_agent_request)
    assert resp == eval_constants.test_register_agent_response
    with pytest.raises(RuntimeError, match='Failed to register agent: 400 - test_error'):
        mocker.patch('aiohttp.ClientSession.post', return_value=get_400_test_obj())
        await agent_info.register_agent_request(eval_constants.test_register_agent_request)

    mocker.patch('local_cloud_agent.agent.agent_info.register_agent_request', return_value=eval_constants.test_register_agent_response)
    await agent_info.register_agent()
    mocker.patch('local_cloud_agent.agent.agent_info.fetch_file_data', return_value=None)
    await agent_info.get_registration()



@pytest.mark.usefixtures("registered_agent")
@pytest.mark.asyncio
async def test_get_registration() -> None:
    from local_cloud_agent.agent import agent_info
    resp = await agent_info.get_registration()
    assert resp == AgentRegisterResponse(
        agent_id=eval_constants.test_agent_id,
        agent_key=eval_constants.test_agent_key,
        ip_address=eval_constants.test_ip_address,
        operations_queue_url=eval_constants.test_operations_queue_url
    )



@pytest.mark.usefixtures("registered_agent")
@pytest.mark.asyncio
async def test_get_agent_state() -> None:
    from local_cloud_agent.agent import agent_info
    expected_agent_state = AgentState(
        agent_id=eval_constants.test_agent_id,
        queue_url=eval_constants.test_operations_queue_url,
        version=eval_constants.test_version
    )
    agent_state = await agent_info.get_agent_state()
    assert expected_agent_state == agent_state
