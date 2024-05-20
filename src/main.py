import asyncio

from cumulonimbus_models.operations import OperationResultStatus

from operations import complete_operation, operations_map, init_operation
from agent import startup
from util import agent_state, logger, aiosession


async def listen_to_queue() -> None:
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
                await sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
                operation_func = operations_map[operation.operation.type]
                try:
                    result = await operation_func(operation)
                except Exception as e:
                    result = str(e)
                    operation.status = OperationResultStatus.FAILURE
                    logger.exception(e)
                finally:
                    await complete_operation(operation, result)
            else:
                await asyncio.sleep(60 * 5)


async def async_main() -> None:
    await startup()
    await listen_to_queue()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()

