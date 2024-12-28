# dimensions_choice.py

import random

ALL_ARGS = ["datapoints", "nbr_dims", "last_dim"]


def alternate_dim(nbr_dims, last_dim, **kwargs):
    """
    Returns the next dimension to split on.
    """
    return {"dim": (last_dim + 1) % nbr_dims}

ALTERNATE_OUT_PLUS = []


def random_dim(nbr_dims, **kwargs):
    """
    Returns a random dimension to split on.
    """
    return {"dim": random.randint(0, nbr_dims - 1)}

RANDOM_OUT_PLUS = []


def max_variance_dim(datapoints: list[list[float]], nbr_dims: int, **kwargs):
    """
    Returns the dimension with the highest variance.
    """
    max_variance = 0
    max_variance_dim = 0

    mean_val = 0

    mean_val_out = 0

    for dim in range(nbr_dims):
        variance = 0
        # calculate the mean value across all points for the current dimension
        mean_val = sum([point[dim] for point in datapoints]) / len(datapoints)

        # calculate the variance
        variance = sum([(point[dim] - mean_val) ** 2 for point in datapoints])
        variance /= len(datapoints)

        if variance > max_variance:
            max_variance = variance
            max_variance_dim = dim
            mean_val_out = mean_val
    return {"dim": max_variance_dim, "mean_val": mean_val_out}

MAX_VARIANCE_OUT_PLUS = ["mean_val"]


def widest_interval_dim(datapoints: list[list[float]], nbr_dims: int, **kwargs):
    """
    Returns the dimension with the highest maximum-minimum value.
    """
    max_range = 0
    max_range_dim = 0

    max_val = 0
    min_val = 0

    for dim in range(nbr_dims):
        max_val = max([point[dim] for point in datapoints])
        min_val = min([point[dim] for point in datapoints])
        range_val = max_val - min_val
        if range_val > max_range:
            max_range = range_val
            max_range_dim = dim
    return {"dim": max_range_dim, "max_val": max_val, "min_val": min_val}

WIDEST_INTERVAL_OUT_PLUS = ["max_val", "min_val"]

DIM_OUT_PLUS = {
    "alternate": ALTERNATE_OUT_PLUS,
    "random": RANDOM_OUT_PLUS,
    "max_variance": MAX_VARIANCE_OUT_PLUS,
    "widest_interval": WIDEST_INTERVAL_OUT_PLUS,
}
