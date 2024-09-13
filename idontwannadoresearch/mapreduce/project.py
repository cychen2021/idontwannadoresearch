from .segment import Segment
from typing import Any, Sequence

class Project[T]:
    def __init__(self, data: Sequence[T]) -> None:
        self.data = data
    
    def project(self) -> Sequence[T]:
        return self.data
    def __call__(self) -> Sequence[T]:
        return self.project()
    def __rshift__(self, segment: Segment) -> Segment:
        segment.project = self
        return segment

def project[T](data: Sequence[T]) -> Project[T]:
    return Project(data)