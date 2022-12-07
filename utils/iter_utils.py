import numpy as np
from typing import Callable


def iterate(func: Callable, V: np.array, n: int = 0, **P) -> np.array:

    if not isinstance(V, np.ndarray):
        return iterate(func, np.array(V), n, **P)
    else:    
        trajectory = [V]
        for t in range(1,n):
            trajectory.append(func(trajectory[-1], **P))
        return np.array(trajectory)
