# Models should have minimal imports
from datetime import datetime
from typing import Any, Callable, Coroutine, Optional

from cumulonimbus_models.operations import Operation, OperationResult, OperationResultStatus
from pydantic import BaseModel


class VersionInfo(BaseModel):
    major: int
    minor: int
    patch: int
    release_candidate: Optional[int] = None

    def __str__(self) -> str:
        if self.release_candidate is None:
            return f'v{self.major}.{self.minor}.{self.patch}'
        else:
            return f'v{self.major}.{self.minor}.{self.patch}-rc{self.release_candidate}'


class AgentState(BaseModel):
    agent_id: str
    queue_url: str
    version: str


class AgentOperation(BaseModel):
    started: datetime
    operation: Operation
    status: OperationResultStatus


PostOperation = Callable[[AgentOperation], Coroutine[Any, Any, None]]


class AgentOperationResult(BaseModel):
    operation_result: OperationResult
    post_op: Optional[PostOperation] = None


OperationFunc = Callable[[AgentOperation], Coroutine[Any, Any, AgentOperationResult]]