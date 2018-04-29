from collections import defaultdict
from typing import List
from scipy.spatial.distance import euclidean


def get_kdist_data(data: List[List], min_points):
    distances = get_distances(data)
    knn_distances = get_kth_nearest_neighbors_distances(k=min_points, distances=distances)
    return create_kdist_data(knn_distances)


def get_distances(data: List[List]) -> defaultdict(list):
    distances = defaultdict(list)
    for i, this_point in enumerate(data):
        for point in data:
            d = euclidean(this_point, point)
            if d != 0:
                distances[i].append(d)
        distances[i].sort()
    return distances


def get_kth_nearest_neighbors_distances(k: int, distances: defaultdict(list)):
    kth_nearest_neighbors = []
    for point, distances in distances.items():
        kth_nearest_neighbor = distances[k]
        kth_nearest_neighbors.append(kth_nearest_neighbor)
    return sorted(kth_nearest_neighbors)


def create_kdist_data(kth_nearest_neighbors: List[int]):
    data = []
    for i, distance in enumerate(kth_nearest_neighbors):
        point = (i, distance)
        data.append(point)
    return data
