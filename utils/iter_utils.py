# from typing import Callable

# def iterate(map: Callable, r, x0=[], n=0) -> list:

#     assert isinstance(r, (list, int, float)), 'r must be of type list, int or float'
#     assert isinstance(x0, (list, int, float)), 'x0 must be of type list, int or float'

#     # make sure r and x0 are in array
#     r_list = [r] if isinstance(r, (int, float)) else r
#     x0_list = [x0] if isinstance(x0, (int, float)) else x0
    
#     trajectories = []
#     for r in r_list:
#         for x0 in x0_list:
#             trajectory = [x0]
#             x = x0
#             for i in range(n):
#                 x = map(r, x)
#                 trajectory.append(x)
#             t = (trajectory, r, n)
#             trajectories.append(t)

#     if len(trajectories)==0:
#         return ([], r, 0)
#     elif len(trajectories)==1:
#         return trajectories[0]
#     else:
#         return trajectories