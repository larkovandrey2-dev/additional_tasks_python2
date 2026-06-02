import unittest

from task4 import LazyTable


class TestLazyTable(unittest.TestCase):
    def test_where_select_take(self) -> None:
        rows = [
            {"name": "Ann", "age": 17},
            {"name": "Bob", "age": 20},
            {"name": "Cat", "age": 30},
        ]

        table = (
            LazyTable(rows)
            .where(lambda row: row["age"] >= 18)
            .select(lambda row: row["name"])
            .take(2)
        )

        self.assertEqual(list(table), ["Bob", "Cat"])

    def test_no_work_before_iter(self) -> None:
        calls: list[int] = []
        table = LazyTable([1, 2, 3]).where(lambda value: calls.append(value) or True)

        self.assertEqual(calls, [])
        self.assertEqual(list(table), [1, 2, 3])
        self.assertEqual(calls, [1, 2, 3])

    def test_take_zero(self) -> None:
        calls: list[int] = []

        def numbers():
            for number in range(5):
                calls.append(number)
                yield number

        table = LazyTable(numbers()).take(0)

        self.assertEqual(list(table), [])
        self.assertEqual(calls, [])

    def test_work_with_infinite_source(self) -> None:
        def numbers():
            number = 0
            while True:
                yield number
                number += 1

        table = LazyTable(numbers()).where(lambda value: value % 2 == 0).take(3)

        self.assertEqual(list(table), [0, 2, 4])


if __name__ == "__main__":
    unittest.main()
