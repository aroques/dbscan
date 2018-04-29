from collections import defaultdict
from typing import List
from scipy.spatial.distance import euclidean


def get_kdist_data(data: List[List], min_points) -> List[tuple]:
    """Get kdist data that can be plotted to determine EPS param for DBScan algorithm."""
    distances = get_distances(data)
    knn_distances = get_kth_nearest_neighbors_distances(k=min_points, distances=distances)
    return create_kdist_data(knn_distances)


def get_distances(data: List[List]) -> defaultdict(list):
    """Gets distances of each point to each other point.

    Args:
        data: The data.

    Returns:
        A default dict.
        The key is the ID of the data point, and the values is a list of distances to each other data point.

    """
    distances = defaultdict(list)
    for i, this_point in enumerate(data):
        for point in data:
            d = euclidean(this_point, point)
            if d != 0:
                distances[i].append(d)
        distances[i].sort()
    return distances


def get_kth_nearest_neighbors_distances(k: int, distances: defaultdict(list)) -> List[float]:
    """Gets a sorted list of each data points kth nearest neighbor's distance.

    Args:
        k: The kth closest point.
        distances: A default dict.
        The key is the ID of the data point, and the values is a list of distances to each other data point.

    Returns:
        A sorted list of each data points kth nearest neighbor's distance.

    """
    knn_distances = []
    for point, distances in distances.items():
        kth_nearest_neighbor = distances[k]
        knn_distances.append(kth_nearest_neighbor)
    return sorted(knn_distances)


def create_kdist_data(knn_distances: List[float]):
    """Get kdist data that can be plotted to determine EPS param for DBScan algorithm.

    Args:
        knn_distances: A sorted list of knn distances.

    Returns:
        kdist data.

    """
    data = []
    for i, distance in enumerate(knn_distances):
        point = (i, distance)
        data.append(point)
    return data
