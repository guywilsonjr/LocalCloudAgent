from cumulonimbus_models.operations import OperationType
from local_cloud_agent.agent.operations.update import update_local_cloud_agent, shell_command


operations_map = {
    OperationType.UPDATE: update_local_cloud_agent,
    OperationType.SHELL_COMMAND: shell_command
}
