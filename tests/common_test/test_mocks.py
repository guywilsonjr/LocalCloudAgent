import logging
import os

from common import constants
from tests.common_test import test_constants


class MockAIOHttpResponse:

    def __init__(self):
        self.status = 200

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self
