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


def plot_iterations(P: dict, V: dict, V_fp=None, ax=None, figsize=(16,4), title=False):

    if ax:
        result = ax
    else:
        result = None
        _, ax = plt.subplots(1, 1, figsize=figsize)

    if V:
        ps = '['+ (', '.join(f'{key}:{value:.4g}' for key, value in P.items()) if P else 'NA') + ']'
        v0s = '['+ (', '.join(f'{key}:{value[0]:.4g}' for key, value in V.items()) if V else 'NA') + ']'
        n_iter = max(0, max(len(value) for value in V.values()))

        # plot fixed points
        if V_fp:
            for v_fp in V_fp:
                ax.plot([1, n_iter+1], [v_fp, v_fp], '--b', lw=0.3)
                if len(V_fp)<=4:
                    ax.annotate(f'${v_fp:.3g}$', xy=(n_iter+2,v_fp), xytext=(3, 3), ha='right', fontsize=9, textcoords='offset points')

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


def plot_cobweb(map, P, V, V_fp=None, ax=None, title=False):
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

        # plot fixed points
        if V_fp:
            for v_fp in V_fp:
                ax.plot([v_min, v_max], [v_fp, v_fp], '--b', lw=0.3)
                if len(V_fp)<=4:
                    ax.annotate(f'${v_fp:.3g}$', xy=(v_min,v_fp), xytext=(3, 3), ha='left', fontsize=9, textcoords='offset points')

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
    