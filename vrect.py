"""
pygame Vector Rect

author: Piop2
"""
from typing import Generic, TypeVar

T = TypeVar("T", int, float)

class RangedNumber(Generic[T]):
    def __init__(self, init: T, start: T, end: T) -> None:
        self._n = init
        self._start = start
        self._end = end

    @property
    def start(self) -> T:
        return self._start

    @property
    def end(self) -> T:
        return self._end

    @property
    def range(self) -> T:
        return abs(self._end - self._start)

    def _get_num(self, num: T) -> T:
        while True:
            if num >= self._end:
                num = num - self.range
            elif num < self._start:
                num = self.range + num
            else:
                break
        return num

    def __add__(self, num: T) -> "RangedNumber":
        if not isinstance(num, T):
            raise TypeError
        return RangedNumber(self._get_num(self._n + num), self._start, self._end)

    def __sub__(self, num: T) -> "RangedNumber":
        if not isinstance(num, T):
            raise TypeError
        return RangedNumber(self._get_num(self._n - num), self._start, self._end)

    def __repr__(self) -> str:
        return f"{self._n}"

    def __int__(self) -> int:
        return self._n


class VectorRect:
    pass
