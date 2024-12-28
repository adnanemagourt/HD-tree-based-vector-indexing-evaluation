# group_choice.py

def closest_seed_group(seed:list[float], seed2:list[float], nbr_dims:int, datapoints:list[list[float]]):
    """
    Returns the group of points that are closest to either seed1 or seed2.
    """
    group1 = []
    group2 = []

    for point in datapoints:
        dist1 = sum([(point[dim] - seed[dim]) ** 2 for dim in range(nbr_dims)]) ** 0.5
        dist2 = sum([(point[dim] - seed2[dim]) ** 2 for dim in range(nbr_dims)]) ** 0.5

        if dist1 < dist2:
            group1.append(point)
        else:
            group2.append(point)

    return group1, group2


def sorting_distance_to_one_seed_group(seed:list[float], nbr_dims:int, datapoints:list[list[float]], **kwargs):
    """
    Sorts the points based on the distance from the seed. Then splits the sorted points into two groups.
    """
    sorted_points = sorted(datapoints, key=lambda x: sum([(x[dim] - seed[dim]) ** 2 for dim in range(nbr_dims)]))
    group1 = sorted_points[:len(sorted_points) // 2]
    group2 = sorted_points[len(sorted_points) // 2:]

    return group1, group2
    


