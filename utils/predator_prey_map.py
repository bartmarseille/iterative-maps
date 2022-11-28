def pred_prey_map(P: dict, V: dict) -> dict:
    """
    The implementation of a predator prey system with parameters `P` and variables `V`.

    Parameters `P`: [a, b, c, d, timestep] with:
    - a: birth rate of rabbits
    - b: death rate of rabbits due to predation
    - c: natural death rate of foxes
    - d: factor that describes how many eaten rabbits give birth to a new fox
    - timestep: the time increment for this differential equation

    Variables `V`: [x, y]` with:
    - x: number of rabbits
    - y: number of foxes
    
    Output `V_hat`: [x, y]`.
    """
    
    # Parameter setup
    a = P['a']
    b = P['b']
    c = P['c']
    d = P['d']
    timestep = P['timestep']
    
    # Map the states into local variable names
    x = V['x']
    y = V['y']

    # evaluate the current differentials
    x_hat = x + (x * (a - b * y)) * timestep
    y_hat = y + (-y * (c - d * x)) * timestep

    return {'x': x_hat, 'y': y_hat}