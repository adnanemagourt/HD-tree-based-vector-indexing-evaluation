# split_position_choice.py
import random

ALL_ARGS = ["datapoints", "dim", "sort", "length"]


def mean_split(
    datapoints: list[list[float]], dim: int, mean_val: float = None, **kwargs
):
    """
    Returns the mean value of the given dimension.
    """

    if mean_val is not None:
        return mean_val
    return sum([point[dim] for point in datapoints]) / len(datapoints)


def median_split(
    datapoints: list[list[float]],
    dim: int,
    sort: bool = False,
    length: int = None,
    **kwargs
):
    """
    Returns the median value of the given dimension.
    """
    if not sort:
        sorted_points = sorted(datapoints, key=lambda x: x[dim])
        mid = len(sorted_points) // 2
    else:
        sorted_points = datapoints
        mid = length // 2
    return sorted_points[mid][dim]


def random_split(
    datapoints: list[list[float]], dim: int, sort: bool = False, **kwargs
):
    """
    Returns a random value of the given dimension.
    """

    if not sort:
        sorted_points = sorted(datapoints, key=lambda x: x[dim])
    else:
        sorted_points = datapoints
    split = (
        random.random() * (sorted_points[-1][dim] - sorted_points[0][dim])
        + sorted_points[0][dim]
    )
    return split


def geometric_center_split(
    datapoints: list[list[float]],
    dim: int,
    sort: bool = False,
    max_val: float = None,
    min_val: float = None,
    **kwargs
):
    """
    Returns the geometric center of the given dimension.
    """

    if max_val is not None and min_val is not None:
        return (max_val + min_val) / 2
    if not sort:
        sorted_points = sorted(datapoints, key=lambda x: x[dim])
    else:
        sorted_points = datapoints
    return (sorted_points[0][dim] + sorted_points[-1][dim]) / 2
