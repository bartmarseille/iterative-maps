import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler
from typing import Callable



def init_darkmode():
    mpl.style.use("dark_background")
    # prepend yellow to color_cycle
    color_cycle=['y']+[d['color'] for d in mpl.rcParams['axes.prop_cycle']]
    # mpl.rcParams['axes.prop_cycle'] = cycler(color=color_cycle[:-1])
    mpl.rcParams['axes.prop_cycle'] = cycler(color=color_cycle)


def get_param_str(**parameters):
    if parameters:
        return '['+ (', '.join(f'{k}:{v:.4g}' for k, v in parameters.items())) + ']'
    else:
        return ''


def plot_iterations(T: np.ndarray, fixed_points: list=None, labels=['x','y','z'], title=None, ax=None, figsize=(16,4), **parameters):
    _ax = ax if ax else plt.subplots(1, 1, figsize=figsize)[1]

    # plot fixed points
    if fixed_points:
        n = T.shape[T.ndim-1]
        for fp in fixed_points:
            _ax.plot([1, n+1], [fp, fp], '--b', lw=0.3)
            if len(fixed_points)<=4:
                _ax.annotate(f'${fp:.3g}$', xy=(n+2,fp), xytext=(3, 3), ha='right', fontsize=9, textcoords='offset points')
    # plot trajectories
    if T.ndim > 1:
        for i in range(T.shape[1]):
            plot_iterations(T[:,i], labels=[labels[i]], ax=_ax, **parameters)
    else:
        n = range(1, T.size+1)

        _ax.plot(n, T, marker='.', alpha=0.7, linewidth=1, label=labels[0])
        _ax.set_ylabel(_ax.get_ylabel() + (', ' if _ax.get_ylabel() else '') + f'${labels[0]}$')

    _ax.legend(loc='upper left')
    _ax.set_xlabel(f'$time$ $→$')
    _ax.set_title(title if isinstance(title, str) else f'Trajectory: {get_param_str(**parameters)}')

    if not ax:
        plt.tight_layout()
    return ax


def plot_cobweb(func: Callable, T: np.ndarray, fixed_points: list=None, ax=None, figsize=(4,4), **parameters):
    assert T.ndim==1, 'trajectory should be 1 dimensional'
    _ax = ax if ax else plt.subplots(1, 1, figsize=figsize)[1]
    
    # plot map
    linspace = np.linspace(0., 1., 1000)
    linspace_dot = func(linspace, **parameters)
    _ax.plot(linspace, linspace_dot, c='b', alpha=0.7, lw=1)
    _ax.plot(linspace, linspace, c='b', alpha=0.7, lw=0.7)
    # plot fixed points
    if fixed_points:
        # n = T.shape[T.ndim-1]
        for fp in fixed_points:
            _ax.plot([0., 1.], [fp, fp], '--b', lw=0.3)
            if len(fixed_points)<=4:
                _ax.annotate(f'${fp:.3g}$', xy=(1.,fp), xytext=(3, 3), ha='right', fontsize=9, textcoords='offset points')
    #plot timeseries Trajectory
    for i in range(T.size-2):
        _ax.plot([T[i], T[i]], [T[i], T[i+1]], c='y', alpha=0.7)
        _ax.plot([T[i]], [T[i+1]], 'oy', ms=5, alpha=(i+1)/T.size)
        _ax.plot([T[i], T[i+1]], [T[i+1], T[i+1]], c='y', alpha=0.7)
    _ax.plot([T[-2], T[-2]], [T[-2], T[-1]], c='y', alpha=0.7)
    _ax.plot([T[0]], [T[0]], 'or', ms=5, label=f'$x_{{1}}$')
    c = 'g' if T.size>1 else 'y'
    _ax.plot([T[-2]], [T[-1]], 'og', ms=5, label=f'$x_{{{T.size}}}$')

    _ax.set_title(f'Cobweb: {get_param_str(**parameters)}')
    _ax.set_ylabel('$x_{t+1}$')
    _ax.set_xlabel('$x_{t}$')
    _ax.set_xlim(0., 1.)
    _ax.set_ylim(0., 1.)
    _ax.legend(loc="upper left")
    if not ax:
        plt.tight_layout()
    return ax
    