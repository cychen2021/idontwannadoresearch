from .mailog import Mailogger
from .diagnostic import Diagnostic, diagnose

def watch(logger: Mailogger, message: str | None = None):
    def __watch(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.log('You are doomed!' if message is None else message, str(e))
        return wrapper
    return __watch
