from dimension_choice import *
from split_position_choice import *
from sklearn.metrics import silhouette_score
import numpy as np

class KDTree:
    """
    A class to represent a KDTree.

    Attributes
    ----------
    k : int
        The number of dimensions of the datapoints.
    root : dict
        The root node of the KDTree.
    dimension_choice : function
        The function to choose the dimension to split on.
    split_position_choice : function
        The function to choose the split position.
    leaf_size : int
        The maximum number of points that can be stored in a leaf node.
    max_depth : int
        The maximum depth of the tree.

    Methods
    -------
    build(datapoints: list[list[float]]) -> dict
        Builds the KDTree from the given datapoints.
    recursive_build(datapoints: list[list[float]], depth: int) -> dict
        Recursively builds the KDTree from the given datapoints.
    compute_silhouette_score() -> float
        Computes the Silhouette Score for the KDTree.
    """

    def __init__(
        self,
        k: int,
        datapoints: list[list[float]],
        dimension_choice: str = "random",
        split_position_choice: str = "random",
        leaf_size: int = 10,
        max_depth: int = None,
    ):
        """
        Initializes the KDTree with the given datapoints and the dimension_choice and split_position_choice functions.

        Parameters
        ----------
        datapoints : list[list[float]]
            The list of datapoints to build the KDTree from.
        dimension_choice : str, optional
            The function to choose the dimension to split on, by default "random".
            Options: "alternate", "random", "max_variance", "widest_interval".
        split_position_choice : str, optional
            The function to choose the split position, by default "random".
            Options: "mean", "median", "random", "geometric_center".
        leaf_size : int, optional
            The maximum number of points that can be stored in a leaf node, by default 10.
        max_depth : int, optional
            The maximum depth of the tree, by default None.

        Raises
        ------
        ValueError
            If the dimension_choice or split_position_choice is not a valid function.
        """

        self.k = k
        self.leaf_size = leaf_size
        self.max_depth = max_depth

        switcher: dict[str, function] = {
            "alternate": alternate_dim,
            "random": random_dim,
            "max_variance": max_variance_dim,
            "widest_interval": widest_interval_dim,
        }

        assert dimension_choice in switcher, "Invalid dimension_choice, choose from 'alternate', 'random', 'max_variance', 'widest_interval'"

        self.dimension_choice = switcher[dimension_choice]

        self.dim_out_plus = DIM_OUT_PLUS[dimension_choice]

        switcher = {
            "mean": mean_split,
            "median": median_split,
            "random": random_split,
            "geometric_center": geometric_center_split,
        }

        assert split_position_choice in switcher, "Invalid split_position_choice, choose from 'mean', 'median', 'random', 'geometric_center'"

        self.split_position_choice = switcher[split_position_choice]
        
        self.root = self.build(datapoints)

    def build(self, datapoints):
        if len(datapoints) == 0:
            return None
        return self.recursive_build(datapoints, 0)

    def recursive_build(self, datapoints: list[list[float]], depth: int, last_dim: int = 0):
        # Stop recursion if the number of points is <= leaf_size or max_depth is reached
        if len(datapoints) <= self.leaf_size or (self.max_depth is not None and depth >= self.max_depth):
            return {
                "depth": depth,
                "points": datapoints,
                "leaf": True,
            }

        kwargs = {"datapoints": datapoints, "nbr_dims": self.k, "last_dim": last_dim}
        dim_result = self.dimension_choice(**kwargs)
        split_dim = dim_result["dim"]
        plus = {key: dim_result[key] for key in self.dim_out_plus}

        kwargs = {"datapoints": datapoints, "dim": split_dim}

        split_result = self.split_position_choice(**kwargs, **plus)
        split_val = split_result

        sorted_points = sorted(datapoints, key=lambda x: x[split_dim])

        left_points = []
        right_points = []

        for point in sorted_points:
            if point[split_dim] < split_val:
                left_points.append(point)
            else:
                right_points.append(point)

        if len(left_points) == 0:
            left_child = None
        else:
            left_child = self.recursive_build(left_points, depth + 1, split_dim)

        if len(right_points) == 0:
            right_child = None
        else:
            right_child = self.recursive_build(right_points, depth + 1, split_dim)

        return {
            "split_dim": split_dim,
            "split_val": split_val,
            "left": left_child,
            "right": right_child,
            "depth": depth,
            "leaf": False,
        }

    def compute_silhouette_score(self):
        """
        Computes the Silhouette Score for the KDTree.

        Returns
        -------
        float
            The Silhouette Score of the KDTree.
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
        Flattens the KDTree to get all points and their cluster labels.

        Parameters
        ----------
        node : dict
            The current node of the KDTree.
        label : int
            The current cluster label.

        Returns
        -------
        list[list[float]], list[int]
            The list of points and their cluster labels.
        """
        if node is None:
            return [], []

        if node["leaf"]:
            points = node["points"]
            labels = [label] * len(points)
            return points, labels

        left_points, left_labels = self._flatten_tree(node["left"], label)
        right_points, right_labels = self._flatten_tree(node["right"], label + 1)

        return left_points + right_points, left_labels + right_labels