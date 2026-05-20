from contextlib import contextmanager
import time


@contextmanager
def tracer(name: str):
    start = time.time()
    try:
        yield
    finally:
        duration = time.time() - start
        print(f"[TRACE] {name} took {duration:.4f}s")