from cumulonimbus_models.operations import OperationType
from agent.operations.update import update_local_cloud_agent


operations_map = {
    OperationType.UPDATE: update_local_cloud_agent
}
