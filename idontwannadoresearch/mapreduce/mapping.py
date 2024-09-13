from typing import Callable
from .segment import Segment
from .accumulate import Accumulate
import concurrent.futures

class Mapping[T, R]:
    def __init__(self, mapper: Callable[[T], R], segment: Segment[T] | None) -> None:
        self.mapper = mapper
        self.segment = segment

    def map(self, data: T) -> R:
        return self.mapper(data)
    
    def __call__(self) -> list[R]:
        assert self.segment is not None, "Segment is not set"
        segments = self.segment()
        
        def wrapper(data: list[T]) -> list[R]:
            return list(map(self.map, data))
        
        futures = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future = executor.map(wrapper, segments)
            futures.append(future)
        result = []
        for future in concurrent.futures.as_completed(futures):
            result.extend(future.result())

        return result

    def __rshift__[T1](self, accumulate: Accumulate[R, T1, T]) -> R:
        accumulate.mapping = self
        return accumulate()

def mapping[T, R](mapper: Callable[[T], R]) -> Mapping[T, R]:
    return Mapping(mapper, None)