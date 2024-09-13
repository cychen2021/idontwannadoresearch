from typing import Any, Callable
from .mapping import Mapping

class Accumulate[T, R, T1]:
    def __init__(self, acc: Callable[[list[T]], R], mapping: Mapping[T1, T] | None = None) -> None:
        self.acc = acc
        self.mapping = mapping
        
    def accumulate(self, data: list[T]) -> R:
        return self.acc(data)

    def __call__(self) -> Any:
        assert self.mapping is not None, "Mapping is not set"
        return self.acc(self.mapping())

def accumulate[T, R](acc: Callable[[list[T]], R]) -> Accumulate[T, R, object]:
    return Accumulate(acc, None)
