import time
from typing import Callable, Any, Tuple

def measure_ms(func: Callable[..., Any], *args, repeat: int = 1, **kwargs) -> Tuple[Any, float]:
    """
    Measures the average execution time of a function in milliseconds (averages for repeat>1).
    Returns: (result from the last call, average time in ms).
    """
    start_ns = time.perf_counter_ns()
    result = None
    for _ in range(repeat):
        result = func(*args, **kwargs)
    end_ns = time.perf_counter_ns()
    avg_ms = (end_ns - start_ns) / 1_000_000.0 / max(1, repeat)
    return result, avg_ms