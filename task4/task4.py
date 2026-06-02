from typing import Iterable, Callable, Iterator

class LazyTable:
    def __init__(self, rows: Iterable[object], operations: list[tuple[str, object]] | None = None) -> None:
        self._rows = rows
        self._operations = operations or []

    def where(self, predicate: Callable[[object], bool]) -> "LazyTable":
        return LazyTable(self._rows, self._operations + [("where", predicate)])

    def select(self, mapper: Callable[[object], object]) -> "LazyTable":
        return LazyTable(self._rows, self._operations + [("select", mapper)])

    def take(self, count: int) -> "LazyTable":
        if count < 0:
            raise ValueError("count must be >= 0")
        return LazyTable(self._rows, self._operations + [("take", count)])

    def __iter__(self) -> Iterator[object]:
        iterator = iter(self._rows)

        for operation, argument in self._operations:
            if operation == "where":
                iterator = self._where(iterator, argument)
            elif operation == "select":
                iterator = self._select(iterator, argument)
            elif operation == "take":
                count = argument
                iterator = self._take(iterator, count)

        return iterator

    @staticmethod
    def _where(iterator: Iterator[object], predicate: Callable[[object], bool]) -> Iterator[object]:
        for row in iterator:
            if predicate(row):
                yield row

    @staticmethod
    def _select(iterator: Iterator[object], mapper: Callable[[object], object]) -> Iterator[object]:
        for row in iterator:
            yield mapper(row)

    @staticmethod
    def _take(iterator: Iterator[object], count: int) -> Iterator[object]:
        if count == 0:
            return

        taken = 0
        for row in iterator:
            if taken == count:
                break
            taken += 1
            yield row
