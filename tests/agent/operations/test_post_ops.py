from datetime import datetime

import pytest
from cumulonimbus_models.operations import OperationResult, OperationResultStatus

from local_cloud_agent.agent.models import AgentState, AgentOperation
from local_cloud_agent.agent.operations.util import send_operation_result
from tests.common_test import test_constants, test_mocks


