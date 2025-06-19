from .mailog import MailLogger
from .diagnostic import Diagnostic, diagnose

def watch(logger: MailLogger, 
          error_message: str | None = None,
          *, report_ok: bool = False, ok_message: str | None = None):
    def __watch(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                logger.log('You are doomed!' if error_message is None else error_message, 
                           f'Exception: \n{e!r} \n------\nDiagnostic: \n{diagnose()}')
                raise e
            else:
                if report_ok:
                    logger.log('Successfully completed' if ok_message is None else ok_message)
                return result
        return wrapper
    return __watch
