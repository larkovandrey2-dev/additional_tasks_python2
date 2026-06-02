import asyncio
import unittest

from task5 import AsyncResourcePool, ClosedPoolError


class TestAsyncResourcePool(unittest.IsolatedAsyncioTestCase):
    async def test_acquire_returns_resource(self) -> None:
        pool = AsyncResourcePool(["r1"])

        async with pool.acquire() as resource:
            self.assertEqual(resource, "r1")

    async def test_resource_returns_after_exception(self) -> None:
        pool = AsyncResourcePool(["r1"])

        with self.assertRaises(RuntimeError):
            async with pool.acquire():
                raise RuntimeError("problem")

        async with pool.acquire() as resource:
            self.assertEqual(resource, "r1")

    async def test_second_task_wait(self) -> None:
        pool = AsyncResourcePool(["r1"])
        events: list[str] = []

        async def worker(name: str) -> None:
            async with pool.acquire() as resource:
                events.append(f"{name} got {resource}")
                await asyncio.sleep(0.01)

        await asyncio.gather(worker("first"), worker("second"))

        self.assertEqual(events, ["first got r1", "second got r1"])

    async def test_closed_pool(self) -> None:
        pool = AsyncResourcePool(["r1"])

        await pool.close()

        with self.assertRaises(ClosedPoolError):
            async with pool.acquire():
                pass


if __name__ == "__main__":
    unittest.main()
