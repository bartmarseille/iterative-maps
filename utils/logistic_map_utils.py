# import numpy as np

def logistic_map(r, x):
    """The logistic map models the evolution of a population,
    by mapping the current population size `x_t` to the next `x_t+1`$,
    taking into account both reproduction rate `r` and density-dependent mortality or starvation `(x-1)`,

    Parameters:
    r : the reproduction rate
    x : the current relative population size

    Returns:
    float: the relative population size after a discrete time step

   """
    return r * x * (1 - x)

#rename to convergence
def get_fixed_points(r, n_equilibration_steps=1000, n_sampling_steps=100, epsilon=0.0001, verbose=False):
    """Dependng on the paramenter `r`, the variable `x` of the logistic map converges to:
    - a stable fixed point
    - periodic oscillations between 4 values, 8, 16, 32
    - more complex regimes of aperiodic behavior, interupted by some intervals where most starting values 
    will converge to one or a small number of stable oscillations.

    Parameters:
    r : the reproduction rate
    n_equilibration_steps : number of steps to take before looking for fixed points / limit-cycles (default=1000)
    n_sampling_steps: number of steps used looking for fixed points / limit-cycles (default 100)
    epsilon: floating-point precision threshold for equivalence

    Returns:
    list: a list of non-zero fixed points.
    - If there is only one fixed point, this list will contain one element.
    - If there is a limit cycle, this list will contain all elements in that limit cycle.
    - If there is no limit cycle (i.e. there is chaos), this will return an empty list.

    """
    fixed_points = []

    if r < 1:
        fixed_points =  [0.0]  
    elif r < 3:
        fixed_points = [(r-1)/r]
    elif r == 3.0:
        # hardcoded as convergence is is dramatically slow
        fixed_points = [0.6623452662682413]
    else:  # Periodic or chaotic
        x = 0.5 

        # First, we run 1000 iteration to give the system a chance to settle
        for i in range(n_equilibration_steps):
            x = logistic_map(r, x)

        # Determine number of unique points we encounter in the subsequent `n_sampling_steps`
        for i in range(n_sampling_steps):
            x = logistic_map(r, x)

            # Check whether, up to numerical accuracy, our new $x$ is already in this array.
            x_in_fixed_points = False
            j = 0
            while j < len(fixed_points) and not x_in_fixed_points:
                x_in_fixed_points = abs(fixed_points[j]-x) < epsilon
                j+=1
            
            # If we have not already included x in our fixed points array, then we add it.
            if not x_in_fixed_points:
                fixed_points.append(x) 

    # If our array of fixed points is longer than our preset `maxCycleLength`, then we assume
    # the behavior is chaotic, and return nothing. Otherwise, we return the list.

    if verbose:
        n_fp = len(fixed_points)
        print(f'{n_fp} fixed_point{"s" if n_fp > 1 else ""}: {fixed_points[0] if n_fp == 1 else fixed_points}')
    return fixed_points