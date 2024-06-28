from cumulonimbus_models.operations import OperationResult

from agent.configuration import agent_config
from agent.models import AgentState, PersistedOperation
from agent.operations.send import send_operation_result
from agent.util import append_data_to_file


async def complete_operation(agent_state: AgentState, operation: PersistedOperation, output: OperationResult) -> None:
    await append_data_to_file(agent_config.operation_log_fp, operation.model_dump_json() + '\n')
    await send_operation_result(agent_state, operation, output)

