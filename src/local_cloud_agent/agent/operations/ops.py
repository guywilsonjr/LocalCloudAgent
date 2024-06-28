from cumulonimbus_models.operations import OperationType
from agent.operations.update import update_repository


operations_map = {
    OperationType.UPDATE: update_repository
}
