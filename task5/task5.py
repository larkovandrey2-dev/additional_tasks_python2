
import asyncio
class ClosedPoolError(RuntimeError):
    pass


class _PoolResource:
    def __init__(self, pool: "AsyncResourcePool") -> None:
        self.pool = pool
        self.resource: object | None = None

    async def __aenter__(self) -> object:
        if self.pool._closed:
            raise ClosedPoolError("pool is closed")

        self.resource = await self.pool._queue.get()
        return self.resource

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.pool._queue.put_nowait(self.resource)


class AsyncResourcePool:
    def __init__(self, resources: list[object]) -> None:
        self._queue: asyncio.Queue[object] = asyncio.Queue()
        self._closed = False

        for resource in resources:
            self._queue.put_nowait(resource)

    def acquire(self) -> "_PoolResource":
        return _PoolResource(self)

    async def close(self) -> None:
        self._closed = True