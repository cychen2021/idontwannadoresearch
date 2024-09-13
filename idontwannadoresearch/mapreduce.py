from typing import Any, Sequence, Callable
import concurrent.futures

class Project[T]:
    def __init__(self, data: Sequence[T]) -> None:
        self.data = data
    
    def project(self) -> Sequence[T]:
        return self.data
    def __call__(self) -> Sequence[T]:
        return self.project()
    

    def __rshift__(self, segment: 'Segment[T]') -> 'Segment[T]':
        segment.project = self
        return segment

def project[T](data: Sequence[T]) -> Project[T]:
    return Project(data)

class Segment[T]:
    def __init__(self, seg_num: int, project: Project[T] | None = None) -> None:
        self.seg_num = seg_num
        self.project = project
    
    def seg(self, data: Sequence[T]) -> list[list[T]]:
        base_seg_size = len(data) // self.seg_num
        residue = len(data) % self.seg_num
        
        result = []
        for i in range(0, self.seg_num):
            result.append(data[i * base_seg_size:(i + 1) * base_seg_size])
        if residue > 0:
            result[-1].extend(data[-residue:])
        return result
        
    def __call__(self) -> list[list[T]]:
        assert self.project is not None, "Project is not set"
        return self.seg(self.project.project())
    
    def __rshift__[R](self, mapping: Mapping[T, R]) -> Mapping[T, R]:
        mapping.segment = self
        return mapping
    
def segment(seg_num: int) -> Segment:
    return Segment(seg_num, None)


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


class Accumulate[T, R]:
    def __init__(self, acc: Callable[[list[T]], R], mapping: Mapping[Any, T] | None = None) -> None:
        self.acc = acc
        self.mapping = mapping
        
    def accumulate(self, data: list[T]) -> R:
        return self.acc(data)

    def __call__(self) -> Any:
        assert self.mapping is not None, "Mapping is not set"
        return self.acc(self.mapping())

def accumulate[T, R](acc: Callable[[list[T]], R]) -> Accumulate[T, R]:
    return Accumulate(acc, None)


