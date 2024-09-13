from dataclasses import dataclass
import shutil
import os

@dataclass
class Diagnostic:
    total_disk: int
    used_disk: int
    free_disk: int
    
    def __str__(self) -> str:
        gb_total_disk = self.total_disk / 1024 / 1024 / 1024
        gb_used_disk = self.used_disk / 1024 / 1024 / 1024
        gb_free_disk = self.free_disk / 1024 / 1024 / 1024
        return f'Total disk: {gb_total_disk:.2f} GB\nUsed disk: {gb_used_disk:.2f} GB\nFree disk: {gb_free_disk:.2f} GB'

    @staticmethod
    def get() -> 'Diagnostic':
        t, u, f = shutil.disk_usage(os.getcwd())
        return Diagnostic(t, u, f)

def diagnose() -> Diagnostic:
    return Diagnostic.get()
