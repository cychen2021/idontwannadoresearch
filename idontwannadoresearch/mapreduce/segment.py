from typing import Sequence
from .project import Project
from .mapping import Mapping

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

