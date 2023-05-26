import threading
from functools import wraps

def run_in_thread(*func_args, **func_kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.start()
            return thread
        return wrapper
    return decorator