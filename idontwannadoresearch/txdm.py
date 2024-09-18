from datetime import datetime
from typing import TextIO
import sys

class txdm[T]:
    def __init__(self, total: int, file: TextIO = sys.stderr, desc=None, unit=None) -> None:
        self.start_time = None
        self.total = total
        self.file = file
        self.current = 0
        self.desc = desc
        self.unit = unit
        self.start()
    
    def start(self) -> None:
        self.start_time = datetime.now()
        self.current = 0
    
    def __enter__(self) -> None:
        pass
    
    def close(self) -> None:
        pass
        
    def __exit__(self, *args) -> None:
        self.close()

    def update(self, increment: int=1):
        assert self.start_time is not None, "Call start() first"
        self.current += increment
        elapsed = datetime.now() - self.start_time
        rate = self.current / elapsed.total_seconds()
        remaining = (self.total - self.current) / rate
        unit = 'it' if self.unit is None else self.unit
        desc = '' if self.desc is None else f'[{self.desc}]'
        self.file.write(f"\r{desc}{self.current}/{self.total} ({rate:.2f} {unit}/s, {remaining:.2f} s remaining)")
        self.file.flush()
    