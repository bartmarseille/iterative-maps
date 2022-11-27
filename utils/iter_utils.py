from typing import Callable


def iterate(map: Callable, P: dict, V: dict=None, n=0) -> dict:

    if not V or n<1:
        return {}    
    else:
        # init trajectories with start value at t=0
        trajectories = { key: [value] for key, value in V.items()}
        for _ in range(n-1):
            V_hat = map(P, V)
            for key, value in V_hat.items():
                trajectories[key].append(value)
            V = V_hat
        return trajectories