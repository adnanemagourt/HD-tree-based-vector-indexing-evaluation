from seeds_choice import *
from grouping_choice import *
from sklearn.metrics import silhouette_score
import numpy as np

class RTree:
    """
    RTree class

    Attributes:
    ----------
    k : int
        The number of dimensions of the datapoints.
    root : dict
        The root node of the RTree.
    grouping_choice : function
        The function to choose the grouping of points.
    seed_choice : function
        The function to choose the seed points.
    dimension_choice : str
        The function to choose the dimension to split on.

    Methods:
    -------
    build(datapoints: list[list[float]]) -> dict
        Builds the RTree from the given datapoints.
    recursive_build(datapoints: list[list[float]], depth: int, last_dim: int) -> dict
        Recursively builds the RTree from the given datapoints.
    compute_silhouette_score() -> float
        Computes the Silhouette Score for the RTree.
    _flatten_tree(node: dict, label: int) -> list[list[float]], list[int]
        Flattens the RTree to get all points and their cluster labels.
    """

    def __init__(
        self,
        k: int,
        datapoints: list[list[float]],
        grouping_choice: str = "closest_seed",
        seed_choice: str = "one_dim_farthest",
        dimension_choice: str = "random",
        leaf_size: int = 10,
        max_depth: int = None,
    ):
        """
        Initializes the RTree with the given datapoints and the grouping_choice and seed_choice functions.

        Parameters
        ----------
        k : int
            The number of dimensions of the datapoints.
        datapoints : list[list[float]]
            The list of datapoints to build the RTree from.
        grouping_choice : str, optional
            The function to choose the grouping of points, by default "closest_seed_group".
            Options: "closest_seed_group", "sorting_distance_to_one_seed_group".
        seed_choice : str, optional
            The function to choose the seed points, by default "one_dim_farthest".
            Options: "one_dim_farthest", "farthest_euc_distance".
        dimension_choice : str, optional
            Used by the seed_choice function when it's "one_dim_farthest", by default "random".
            Options: "alternate", "random", "max_variance", "widest_interval".
        leaf_size : int, optional
            The maximum number of points that can be stored in a leaf node, by default 10.
        max_depth : int, optional
            The maximum depth of the tree, by default None.
        """
        self.k = k
        self.leaf_size = leaf_size
        self.max_depth = max_depth

        switcher: dict[str, function] = {
            "closest_seed": closest_seed_group,
            "sorting_distance_to_one_seed": sorting_distance_to_one_seed_group,
        }
        self.grouping_choice = switcher[grouping_choice]

        switcher = {
            "one_dim_farthest": one_dim_farthest_seeds,
            "farthest_euc_distance": farthest_euc_distance_seeds,
        }
        self.seed_choice = switcher[seed_choice]

        self.dimension_choice = dimension_choice

        self.root = self.build(datapoints)

    def build(self, datapoints: list[list[float]]) -> dict:
        """
        Builds the RTree from the given datapoints.

        Parameters
        ----------
        datapoints : list[list[float]]
            The list of datapoints to build the RTree from.
        """
        Pmin = [min(point[dim] for point in datapoints) for dim in range(self.k)]
        Pmax = [max(point[dim] for point in datapoints) for dim in range(self.k)]

        return {
            "min": Pmin,
            "max": Pmax,
            "points": datapoints,
            "depth": 0,
            "children": self.recursive_build(datapoints, 1),
        }

    def recursive_build(
        self, datapoints: list[list[float]], depth: int, last_dim: int = 0
    ) -> dict:
        # Stop recursion if the number of points is <= leaf_size or max_depth is reached
        if len(datapoints) <= self.leaf_size or (self.max_depth is not None and depth >= self.max_depth):
            return None

        seeds_result = self.seed_choice(
            datapoints=datapoints,
            nbr_dims=self.k,
            dimension_choice_alg=self.dimension_choice,
            last_dim=last_dim,
        )

        seeds = seeds_result["seeds"]

        groups = self.grouping_choice(
            seed=seeds[0], seed2=seeds[1], nbr_dims=self.k, datapoints=datapoints
        )

        Pmin = [min(point[dim] for point in groups[0]) for dim in range(self.k)]
        Pmax = [max(point[dim] for point in groups[0]) for dim in range(self.k)]

        left = {
            "min": Pmin,
            "max": Pmax,
            "points": groups[0],
            "depth": depth,
            "children": self.recursive_build(
                groups[0],
                depth + 1,
                last_dim=seeds_result["dim"] if "dim" in seeds_result else None,
            ),
        }

        Pmin = [min(point[dim] for point in groups[1]) for dim in range(self.k)]
        Pmax = [max(point[dim] for point in groups[1]) for dim in range(self.k)]

        right = {
            "min": Pmin,
            "max": Pmax,
            "points": groups[1],
            "depth": depth,
            "children": self.recursive_build(
                groups[1],
                depth + 1,
                last_dim=seeds_result["dim"] if "dim" in seeds_result else None,
            ),
        }

        return {"left": left, "right": right}

    def compute_silhouette_score(self):
        """
        Computes the Silhouette Score for the RTree.

        Returns
        -------
        float
            The Silhouette Score of the RTree.
        """
        # Flatten the tree to get all points and their cluster labels
        points, labels = self._flatten_tree(self.root, 0)
        points = np.array(points)
        labels = np.array(labels)

        # Compute the Silhouette Score
        score = silhouette_score(points, labels)
        return score

    def _flatten_tree(self, node, label):
        """
        Flattens the RTree to get all points and their cluster labels.

        Parameters
        ----------
        node : dict
            The current node of the RTree.
        label : int
            The current cluster label.

        Returns
        -------
        list[list[float]], list[int]
            The list of points and their cluster labels.
        """
        if node is None:
            return [], []

        if "children" not in node or node["children"] is None:
            points = node["points"]
            labels = [label] * len(points)
            return points, labels

        left_points, left_labels = self._flatten_tree(node["children"]["left"], label)
        right_points, right_labels = self._flatten_tree(node["children"]["right"], label + 1)

        return left_points + right_points, left_labels + right_labels