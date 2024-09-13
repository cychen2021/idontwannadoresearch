from typing import Callable, Sequence
from .segment import Segment
from .accumulate import Accumulate
import concurrent.futures

class Mapping[T, R]:
    def __init__(self, mapper: Callable[[Sequence[T]], R], segment: Segment[T] | None) -> None:
        self.mapper = mapper
        self.segment = segment

    def map(self, data: Sequence[T]) -> R:
        return self.mapper(data)
    
    def __call__(self) -> list[R]:
        assert self.segment is not None, "Segment is not set"
        segments = self.segment()
        
        futures = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=len(segments)) as executor:
            future = executor.map(self.map, segments)
            futures.append(future)
        assert len(futures) == len(segments), "Length of futures and segments are not equal"
        result = []
        for future in concurrent.futures.as_completed(futures):
            result.extend(future.result())

        return result

    def __rshift__[R1](self, accumulate: Accumulate[R, R1]) -> R:
        accumulate.mapping = self
        return accumulate()

def mapping[T, R](mapper: Callable[[Sequence[T]], R]) -> Mapping[T, R]:
    return Mapping(mapper, None)