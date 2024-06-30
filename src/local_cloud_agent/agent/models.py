from datetime import datetime
from typing import Awaitable, Optional

from cumulonimbus_models.operations import Operation, OperationResult, OperationResultStatus
from pydantic import BaseModel, ConfigDict


class AgentState(BaseModel):
    agent_id: str
    queue_url: str
    version: str


class AgentOperation(BaseModel):
    started: datetime
    operation: Operation
    status: OperationResultStatus


class AgentOperationResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    operation_result: OperationResult
    post_op: Optional[Awaitable] = None


