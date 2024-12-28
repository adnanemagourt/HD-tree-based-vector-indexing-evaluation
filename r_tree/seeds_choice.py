# seeds_choice.py

from dimension_choice import *


def one_dim_farthest_seeds(
    datapoints: list[list[float]],
    nbr_dims: int,
    dimension_choice_alg: str = "random",
    last_dim: int = None,
    **kwargs
):
    """
    Returns the seeds that are the farthest apart from each other on a single dimension.
    """

    switcher: dict[str, function] = {
        "alternate": alternate_dim,
        "random": random_dim,
        "max_variance": max_variance_dim,
        "widest_interval": widest_interval_dim,
    }

    assert (
        dimension_choice_alg in switcher
    ), "Invalid dimension_choice_alg, choose from 'alternate', 'random', 'max_variance', 'widest_interval'"

    dimension_choice = switcher[dimension_choice_alg]

    dim_result = dimension_choice(datapoints=datapoints, nbr_dims=nbr_dims, last_dim=last_dim)

    chosen_dim = dim_result["dim"]

    max_point = max(datapoints, key=lambda x: x[chosen_dim])
    min_point = min(datapoints, key=lambda x: x[chosen_dim])

    return {"seeds": [max_point, min_point], "dim": chosen_dim}


def farthest_euc_distance_seeds(
    datapoints: list[list[float]],
    nbr_dims: int,
    **kwargs
):
    """
    Returns the seeds that are the farthest apart from each other on all dimensions.
    """

    max_dist = 0
    max_dist_points = []

    for point1 in datapoints:
        for point2 in datapoints:
            dist = sum([(point1[dim] - point2[dim]) ** 2 for dim in range(nbr_dims)]) ** 0.5
            if dist > max_dist:
                max_dist = dist
                max_dist_points = [point1, point2]

    return {"seeds": max_dist_points}
