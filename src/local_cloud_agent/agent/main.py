import asyncio

from cumulonimbus_models.operations import OperationResult, OperationResultStatus

from agent import initialize
from agent.operations.post_ops import complete_operation
from agent.operations.util import init_operation
from agent.operations.ops import operations_map
from agent.agent_info import get_agent_state
from agent.models import AgentOperationResult, AgentState
from agent.util import aiosession
from agent.initialize import logger


async def listen_to_queue(agent_state: AgentState) -> None:
    logger.info('Listening to queue')
    async with aiosession.client('sqs') as sqs:
        queue_url = agent_state.queue_url
        while True:
            response = await sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20
            )

            if 'Messages' in response:
                logger.info('Received message')
                message = response['Messages'][0]
                operation = await init_operation(message)
                logger.info(f'Received operation: {operation}')
                await sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
                operation_func = operations_map[operation.operation.type]
                try:
                    result = await operation_func(operation)
                except Exception as e:
                    result = AgentOperationResult(
                        operation_result=OperationResult(
                            operation_output=str(e),
                            operation_status=OperationResultStatus.FAILURE
                        )
                    )
                    operation.status = OperationResultStatus.FAILURE
                    logger.exception(e)
                finally:
                    if result.post_op:
                        logger.info(f'Running post operation for operation: {operation}')
                        await result.post_op
                    await complete_operation(agent_state, operation, result)
            else:
                await asyncio.sleep(60)


async def async_main() -> None:
    initialize.validate_fs()
    await initialize.startup()
    agent_state = await get_agent_state()
    await listen_to_queue(agent_state)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()

