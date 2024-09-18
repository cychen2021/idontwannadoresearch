from datetime import datetime
from typing import TextIO
import sys

class txdm[T]:
    def __init__(self, total: int, file: TextIO = sys.stderr) -> None:
        self.start_time = None
        self.total = total
        self.file = file
        self.current = 0
    
    def start(self) -> None:
        self.start_time = datetime.now()
        self.current = 0
    
    def __enter__(self) -> None:
        self.start()
        
    def __exit__(self, *args) -> None:
        pass

    def update(self, increment: int):
        assert self.start_time is not None, "Call start() first"
        self.current += increment
        elapsed = datetime.now() - self.start_time
        rate = self.current / elapsed.total_seconds()
        remaining = (self.total - self.current) / rate
        self.file.write(f"\r{self.current}/{self.total} ({rate:.2f} it/s, {remaining:.2f} s remaining)")
        self.file.flush()
    