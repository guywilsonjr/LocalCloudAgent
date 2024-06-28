import asyncio

from cumulonimbus_models.operations import OperationResult, OperationResultStatus

import initialize
from operations.util import complete_operation, init_operation
from operations.ops import operations_map
from agent.agent_info import get_agent_state
from models import AgentState
from util import aiosession
from initialize import logger


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
                    result = OperationResult(operation_output=str(e), operation_status=OperationResultStatus.FAILURE)
                    operation.status = OperationResultStatus.FAILURE
                    logger.exception(e)
                finally:
                    if operation.operation.type == 'UPDATE':
                        logger.info('Update Complete. Restarting')
                        exit(0)
                    else:
                        await complete_operation(operation, result)
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

