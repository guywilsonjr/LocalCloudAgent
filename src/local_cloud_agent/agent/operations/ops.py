from cumulonimbus_models.operations import OperationTypes
from local_cloud_agent.agent.operations.update import update_local_cloud_agent, shell_command


operations_map = {
    OperationTypes.UPDATE: update_local_cloud_agent,
    OperationTypes.SHELL_COMMAND: shell_command
}
