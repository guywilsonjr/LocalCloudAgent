from cumulonimbus_models.operations import OperationResult

from local_cloud_agent.common.configuration import agent_config
from local_cloud_agent.agent.models import AgentState, AgentOperation
from local_cloud_agent.agent.operations.send import send_operation_result
from local_cloud_agent.agent.util import append_data_to_file


async def complete_operation(agent_state: AgentState, operation: AgentOperation, output: OperationResult) -> None:
    await append_data_to_file(agent_config.operation_log_fp, operation.model_dump_json() + '\n')
    await send_operation_result(agent_state, operation, output)

