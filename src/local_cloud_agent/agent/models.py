from datetime import datetime

from cumulonimbus_models.operations import Operation, OperationResultStatus
from pydantic import BaseModel


class AgentState(BaseModel):
    agent_id: str
    queue_url: str
    version: str



class PersistedOperation(BaseModel):
    started: datetime
    operation: Operation
    status: OperationResultStatus



