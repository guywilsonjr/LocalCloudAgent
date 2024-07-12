import asyncio

from cumulonimbus_models.operations import OperationResult, OperationResultStatus
from types_aiobotocore_sqs import SQSClient
from types_aiobotocore_sqs.type_defs import MessageTypeDef, ReceiveMessageResultTypeDef

from agent import initialize
from agent.operations.post_ops import complete_operation
from agent.operations.util import init_operation
from agent.operations.ops import operations_map
from agent.agent_info import get_agent_state
from agent.models import AgentOperation, AgentOperationResult, AgentState, OperationFunc, PostOperation
from agent.util import aiosession
from agent.post_config import logger


async def get_sqs_response(sqs: SQSClient, queue_url: str) -> ReceiveMessageResultTypeDef:
    return await sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )


async def receive_message(sqs: SQSClient, queue_url: str, operation: AgentOperation, message: MessageTypeDef) -> OperationFunc:
    logger.info(f'Received operation: {operation}')
    await sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=message['ReceiptHandle']
    )
    return operations_map[operation.operation.type]


async def execute_operation(agent_state: AgentState, operation_func: OperationFunc, operation: AgentOperation) -> None:
    result = AgentOperationResult(
        operation_result=OperationResult(
            operation_output='Operation not executed',
            operation_status=OperationResultStatus.FAILURE
        )
    )
    try:
        result = await operation_func(operation)
    except Exception as e:
        result.operation_result.operation_output = str(e)
        logger.exception(e)
    finally:
        # TODO add post operation handling on case of failure I think or undo if checking
        if result.post_op:
            logger.info(f'Running post operation for operation: {operation}')
            await result.post_op(operation)
        await complete_operation(agent_state, operation, result.operation_result)


async def poll_queue(agent_state: AgentState, sqs: SQSClient, queue_url: str) -> None:
    response = await get_sqs_response(sqs, queue_url)
    if message := response['Messages'][0] if response['Messages'] else None:
        logger.info('Received message')
        operation = await init_operation(message)
        operation_func = await receive_message(sqs, queue_url, operation, message)
        await execute_operation(agent_state, operation_func, operation)
    else:
        await asyncio.sleep(60)


async def listen_to_queue(agent_state: AgentState) -> None:
    logger.info('Listening to queue')
    async with aiosession.client('sqs') as sqs:
        queue_url = agent_state.queue_url
        while True:
            await poll_queue(agent_state, sqs, queue_url)


async def async_main() -> None:
    agent_state = await get_agent_state()
    await initialize.startup(agent_state)
    await listen_to_queue(agent_state)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()

