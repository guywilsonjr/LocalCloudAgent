from cumulonimbus_models.operations import OperationResult

from common.configuration import agent_config
from agent.models import AgentState, AgentOperation
from agent.operations.send import send_operation_result
from agent.util import append_data_to_file


async def complete_operation(agent_state: AgentState, operation: AgentOperation, output: OperationResult) -> None:
    await append_data_to_file(agent_config.operation_log_fp, operation.model_dump_json() + '\n')
    await send_operation_result(agent_state, operation, output)

