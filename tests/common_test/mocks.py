

class MockAIOHttpResponse:

    def __init__(self) -> None:
        self.status = 200

    async def __aexit__(self, exc_type, exc, tb) -> None:
        pass

    async def __aenter__(self) -> 'MockAIOHttpResponse':
        return self
