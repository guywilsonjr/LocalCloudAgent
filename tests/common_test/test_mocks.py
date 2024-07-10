import logging
import os

from common import constants
from tests.common_test import test_constants


class MockSystemdUnit:

    def __init__(self, *args, **kwargs):
        pass

    def load(self):
        pass

    class UnitUnit:

        def __init__(self, *args, **kwargs):
            pass

        @staticmethod
        def Restart(self, *args, **kwargs):
            pass

    Unit = UnitUnit()



class MockAIOHttpResponse:

    def __init__(self):
        self.status = 200

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self
