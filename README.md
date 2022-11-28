# Iterative maps

A `dynamical system` is a model describing the evolution of an object over time. Using discrete timesteps, the objects temporal evolution is defined by a `rule` or `map` describing the state of the object from time $t$ to time $t+1$. Repeatedly applying a map to an object is called a `iterated map`.

The basic idea of a `iterated map` is to take a number $x_0$ for $t=0$, the `initial condition`, and then in a sequence of $n$ steps to update this number according to a fixed rule or map to obtain a `trajectory`. This project explores this idea of `iterated map`s and shows some quite unexpected properties.

## Iterative map framework

In this project a [general framework](0. Map-iterate-plot-framework.ipynb) for defining, analyzing and visualizing iterable maps is presented.

## Logistic map and chaos

Also, an in-depth analysis of the properties of the [logistic map](1. Logistic-map-and-chaos.ipynb) is included to show the framework in action.
