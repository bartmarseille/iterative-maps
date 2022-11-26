import numpy as np
import math
import matplotlib.pyplot as plt


def plot_iterated_map(map, x0, r, n, ax=None):
    x = np.linspace(0, 1)
    y = map(x, r)
    ax.plot(x, y, c='b', lw=2)
    ax.plot(x, x, c='b', lw=1)

    if n==0:
        ax.plot([x0], [0], 'oy', ms=5, alpha=0)
        ax.set_title(f'$r={r:.1f}$')
    else:
        # Recursively apply y=f(x) and plot two lines:
        # (x, x) -> (x, y)
        # (x, y) -> (y, y)
        y0 = map(x0, r)
        ax.plot([x0, x0], [0, y0], c='y', lw=1)
        ax.plot([x0], [0], 'oy', ms=5, alpha=1/n)

        x = x0
        for i in range(n):
            y = map(x, r)
            ax.plot([x, x], [x, y], c='y', lw=1)
            if i < n-1:
                ax.plot([x, y], [y, y], c='y', lw=1)
            # Plot the positions with increasing opacity.
            ax.plot([x], [y], 'oy', ms=5, alpha=(i + 1) / n)
            x = y
        ax.set_title(f'$r={r:.1f}, \, x_0={x0:.1f}, \, n={n}$')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    

def plot_map(x, y, r):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(1, 1, figsize=(6,6))
    ax.plot(x, y,  c='b', linewidth=1.5)
    ax.plot(x, x,  c='b', linewidth=1)
    ax.set_title(f'r = {r}')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)


def plot_trajectory(map, x0, r, n):
    t = [x0]
    x = x0
    for i in range(n):
        x = map(x, r)
        t.append(x)

    # trajectory = iterate(logistic_map, x0, r, n)

    plt.style.use("dark_background")
    plt.figure(figsize=(20,4))
    plt.plot(t, marker='.', c='y', lw=1)
    plt.xlabel(f'$time$ $→$')
    plt.title(f'$r={r:.1f}, \, x_0={x0:.1f}, \, n={n}$')
    plt.show()


def plot_trajectories(trajectories, n_cols=3):

    plt.style.use("dark_background")

    n_rows = math.ceil(len(trajectories)/n_cols)

    fig, axs = plt.subplots(n_rows, n_cols, figsize=(20,4*n_rows))

    for i, (trajectory, r) in enumerate(trajectories):
        row = int(i/n_cols)
        col = i%n_cols
        
        axs[row, col].plot(trajectory, marker='.', c='y', lw=1)
        axs[row, col].set_title(f'r = {r}')
    
    for ax in axs.flat:
        ax.label_outer()
