import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler


def init_darkmode():
    mpl.style.use("dark_background")
    # prepend yellow to color_cycle
    color_cycle=['y']+[d['color'] for d in mpl.rcParams['axes.prop_cycle']]
    # mpl.rcParams['axes.prop_cycle'] = cycler(color=color_cycle[:-1])
    mpl.rcParams['axes.prop_cycle'] = cycler(color=color_cycle)


def plot_iterations(P: dict, V: dict, ax=None, figsize=(16,4), title=False):

    if ax:
        result = ax
    else:
        result = None
        _, ax = plt.subplots(1, 1, figsize=figsize)

    if V:
        ps = '['+ (', '.join(f'{key}:{value:.4g}' for key, value in P.items()) if P else 'NA') + ']'
        v0s = '['+ (', '.join(f'{key}:{value[0]:.4g}' for key, value in V.items()) if V else 'NA') + ']'
        n_iter = max(0, max(len(value) for value in V.values()))

        ylabels=[]
        x = range(1, n_iter+1)
        for key, y in V.items():
            ax.plot(x, y, marker='.', lw=1,label=f'${key} \, | \, p={ps}, \, V_0={v0s}$')
            ylabels.append(f'${key}_t$')
        ax.set_xlabel(f'$time$ $→$')
        ax.set_ylabel(' / '.join(ylabels))
        if n_iter < 40:
            ax.set_xticks(x)

        ax.legend(loc="upper left")
        if title:
            if isinstance(title, str):
                ax.set_title(title)
            else:
                ax.set_title('Trajector'+('ies' if len(V)>1 else 'y'))
        if result is None:
            plt.tight_layout()
    return result


def plot_cobweb(map, P, V, ax=None, title=False):
    """
    A cobweb plot, or Verhulst diagram is a visual tool used in the dynamical systems 
    field of mathematics to investigate the qualitative behaviour of one-dimensional 
    iterated functions, such as the logistic map. 
    
    Using a cobweb plot, it is possible to infer the long term status of an initial 
    condition under repeated application of a map.
    """

    if not ax:
            _, ax = plt.subplots(1, 1, figsize=(4, 4))
            result = None
    else:
        result = ax

    # check map is 1D, has one variable only
    # and get bounds of the maps variable
    if V and len(V.keys())==1:

        key = list(V.keys())[0]
        v = V[key]

        v_min = min(0.0, min(v))
        v_max = max(1.0, max(v))

        # plot mapping
        V_map = V.copy()
        V_map[key] = np.linspace(v_min, v_max)

        v_map = V_map[key]
        v_map_hat = map(P, V_map)[key]
        ax.plot(v_map, v_map_hat, c='b', lw=2)
        ax.plot(v_map, v_map, c='b', lw=1)

        n = len(V[key])
        if n==1:
            ax.plot([v[0]], [v[0]], 'oy', ms=5)
            # ax.set_title(f'$r={r:.1f}, \, x_0={t[0]:.2g}$')
        else:
            # Recursively apply y=f(x) and plot two lines:
            # (x, x) -> (x, y)
            # (x, y) -> (y, y)
            for i in range(n-2):
                ax.plot([v[i], v[i]], [v[i], v[i+1]], c='y', lw=1)
                ax.plot([v[i]], [v[i+1]], 'oy', ms=5, alpha=(i+1)/n)
                ax.plot([v[i], v[i+1]], [v[i+1], v[i+1]], c='y', lw=1)
            ax.plot([v[-2], v[-2]], [v[-2], v[-1]], c='y', lw=1)
            ax.plot([v[0]], [v[0]], 'or', ms=5)
            c = 'g' if n>1 else 'y'
            ax.plot([v[-2]], [v[-1]], color=c, marker='o', ms=5)
            if title:
                ps = '['+ (', '.join(f'{key}:{value:.4g}' for key, value in P.items()) if P else 'NA') + ']'
                ax.set_title(f'Cobweb: $P={ps}, \, x_0={v[0]:.2g}, \, n={n}$')
            else:
                ax.set_title(f'Cobweb')
    ax.set_ylabel('$x_{t+1}$')
    ax.set_xlabel('$x_{t}$')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    return result 


# def plot_trajectory(t, fixed_points=None, ax=None, figsize=(16,4), labels=False):
    
#     # plt.style.use("dark_background")
#     if ax:
#         result = ax
#     else:
#         result = None
#         _, ax = plt.subplots(1, 1, figsize=figsize)
#     t, r, n = t
#     # ax.plot(t, marker='.', c='y', lw=1)
#     ax.plot(t, marker='.', lw=1)
#     if labels and fixed_points: # and n<=max(figsize)*2:
#         n_fp = len(fixed_points) if isinstance(fixed_points, list) else 1
#         # print(n_fp)
#         if n_fp < 16:
#             n_decimals = 2
#         elif n_fp < 32:
#             n_decimals = 3
#         else: 
#             n_decimals = 1
#         for i, t_ in enumerate(t):
#             # Annotate the points 5 _points_ above and to the left of the vertex
#             ax.annotate('{0:.{1}g}'.format(t_, n_decimals), xy=(i,t_), xytext=(-5, 5), ha='right', textcoords='offset points')
#     ax.set_xlabel(f'$time$ $→$')
#     ax.set_ylabel(f'$x_t$')
#     title = f'$r={r:.6g}, \, x_0={t[0]:.2g}, \, n={n}$'
#     if fixed_points:
#         n_fp = len(fixed_points)
#         if n_fp ==1:
#             fp_text = f'1 stable fixed point at: {fixed_points[0]:.4g}'
#         else:
#             if n_fp in (2,3,4,6,8):
#                 fp_text = f'stable ${n_fp}$ period oscillations: $['+ ', \, '.join([f'{fp:.3g}' for fp in fixed_points]) + ']$'
#             elif n_fp in (12,16,24,32,48,64,96,128,192,256,384,512,768,1024):
#                 fp_text = f'stable ${n_fp}$ period oscillations'
#             else:
#                 fp_text = f'chaos: ossilactions of infinite period.'  # ${n_fp}$.'
#         title = title + ', ' + fp_text
#     ax.set_title(title)
#     if n < 20:
#         ax.set_xticks(range(0, n+1))
#     return result


# def plot_trajectories(trajectories, ax=None, figsize=(16,4), labels=False):
#     # plt.style.use("dark_background")
#     if ax:
#         result = ax
#     else:
#         result = None
#         _, ax = plt.subplots(1, 1, figsize=figsize)
    
#     for i, (t, r, n) in enumerate(trajectories):
#         # plot_trajectory(t, fixed_points=None, ax=None, figsize=(16,4), labels=False)
#         ax.plot(t, marker='.', lw=1,label=f'$r={r:.1f}, \, x_0={t[0]:.1f}, \, n={n}$')
#     ax.set_xlabel(f'$time$ $→$')
#     ax.set_ylabel(f'$x_t$')

#     plt.legend(loc="upper left")
#     if result is None:
#         plt.tight_layout()
#     return result 

# def plot_cobweb(map, trajectory, ax=None):
    
#     # plt.style.use("dark_background")

#     if not ax:
#         _, ax = plt.subplots(1, 1, figsize=(4, 4))

#     # unpack trajectory and parameters
#     (t, r, n) = trajectory

#     # plot mapping
#     x = np.linspace(0, 1)
#     y = map(r, x)
#     ax.plot(x, y, c='b', lw=2)
#     ax.plot(x, x, c='b', lw=1)

#     # plot iteration
#     if not t:
#         ax.set_title(f'$r={r:.1f}$')
#     else:
#         if n==0:
#             ax.plot([t[0]], [t[0]], 'oy', ms=5)
#             ax.set_title(f'$r={r:.1f}, \, x_0={t[0]:.2g}$')
#         else:
#             # Recursively apply y=f(x) and plot two lines:
#             # (x, x) -> (x, y)
#             # (x, y) -> (y, y)
#             for i in range(n-1):
#                 ax.plot([t[i], t[i]], [t[i], t[i+1]], c='y', lw=1)
#                 ax.plot([t[i]], [t[i+1]], 'oy', ms=5, alpha=(i+1)/n)
#                 ax.plot([t[i], t[i+1]], [t[i+1], t[i+1]], c='y', lw=1)
#             ax.plot([t[-2], t[-2]], [t[-2], t[-1]], c='y', lw=1)
#             ax.plot([t[0]], [t[0]], 'or', ms=5)
#             c = 'g' if n>1 else 'y'
#             ax.plot([t[-2]], [t[-1]], color=c, marker='o', ms=5)
#             ax.set_title(f'$r={r:.6g}, \, x_0={t[0]:.2g}, \, n={n}$')
#             ax.set_ylabel('$x_{t+1}$')
#     ax.set_xlabel('$x_{t}$')
#     ax.set_xlim(0, 1)
#     ax.set_ylim(0, 1)


# def plot_trajectory_and_cobweb(map, t, fp=None, axes=None, labels=False):

#     if axes is not None:
#         (ax1, ax2) = axes
#         result = axes
#     else:
#         fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4), gridspec_kw={'width_ratios': [3, 1]}, sharey=True)
#         result = None
#     plot_trajectory(t, fixed_points=fp, ax=ax1, labels=labels)
#     plot_cobweb(map, t, ax2)
#     if result is None:
#         plt.tight_layout()
#     return result


# def plot_trajectories_and_cobweb(map, trajectories, fixed_points=None, labels=False):

#     fig, axes = plt.subplots(1, 2, figsize=(16, 4), gridspec_kw={'width_ratios': [3, 1]}, sharey=True)

#     x0s=[]
#     for trajectory in trajectories:
#         (t, r, n) = trajectory
#         x0s.append(t[0])
#         plot_trajectory_and_cobweb(map, trajectory, fp=fixed_points, axes=axes, labels=labels)

#     x0s_text = f'['+ ', \, '.join([f'{x0:.3g}' for x0 in x0s]) + ']'
#     title = f'$r={r:.6g}, \, x_0={x0s_text}, \, n={n}$'
#     if fixed_points:
#         n_fp = len(fixed_points)
#         if n_fp ==1:
#             fp_text = f'1 stable fixed point at: {fixed_points[0]:.4g}'
#         else:
#             if n_fp in (2,3,4,6,8):
#                 fp_text = f'stable ${n_fp}$ period oscillations: $['+ ', \, '.join([f'{fp:.3g}' for fp in fixed_points]) + ']$'
#             elif n_fp in (12,16,24,32,48,64,96,128,192,256,384,512,768,1024):
#                 fp_text = f'stable ${n_fp}$ period oscillations'
#             else:
#                 fp_text = f'chaos: ossilactions of infinite period.'  # ${n_fp}$.'
#         title = title + ', ' + fp_text
#     axes[0].set_title(title)

#     plt.tight_layout()
