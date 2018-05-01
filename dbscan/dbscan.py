import numpy
from typing import List


class DBSCAN:
    def __init__(self, min_points, epsilon):
        self.min_points = min_points
        self.epsilon = epsilon
        self.point_labels = None
        self.cluster_labels = None

    def fit(self, data):
        data = numpy.array(data)

        labels = [0] * len(data)

        cluster_id = 0

        for point in range(0, len(data)):
            # This loop will ensure we get all the clusters

            if labels[point] != 0:
                # Point is already labeled
                continue

            neighbor_points = self.region_query(data, point)

            if len(neighbor_points) < self.min_points:
                # Noise or border point. Cannot expand this point.
                labels[point] = -1
            else:
                # Point is a core point
                cluster_id += 1
                self.grow_cluster(data, labels, point, neighbor_points, cluster_id)

        return labels

    def grow_cluster(self, data, labels, point, neighbor_points, cluster_id) -> None:
        """Grows the current cluster and assigns labels to any other core or border points.

        neighbor_points can be thought of as a FIFO queue. It will continually grow.
        Once we've expanded all the neighbor points than we know we have maximally
        expanded the current cluster.

        :param data: List of 2d points.
        :param labels: List of labels: 1 for each 2d point in data.
        :param point: Current point in the data set.
        :param neighbor_points: Neighbor points of point.
        :param cluster_id: The current cluster id.
        :return: None
        """
        labels[point] = cluster_id

        i = 0
        while i < len(neighbor_points):

            neighbor_point = neighbor_points[i]

            if labels[neighbor_point] == -1:
                # Relabel the noise point as belonging to this cluster (i.e., border point)
                labels[neighbor_point] = cluster_id

            elif labels[neighbor_point] == 0:
                labels[neighbor_point] = cluster_id

                neighbor_point_neighborhood = self.region_query(data, neighbor_point)

                if len(neighbor_point_neighborhood) >= self.min_points:
                    # This neighborhood has more than min_points,
                    # So add it the neighbor_points FIFO queue
                    neighbor_points += neighbor_point_neighborhood

            i += 1

    def region_query(self, data, this_point) -> List[List]:
        """Queries for list of 2d points that are in the epsilon neighborhood of this_point.

        :param data: List of 2d points.
        :param this_point: Point who's region will be queried
        :return: List of 2d points that are in the epsilon neighborhood of this_point.
        """
        neighbors = []

        for point in range(0, len(data)):

            if numpy.linalg.norm(data[this_point] - data[point]) < self.epsilon:
                neighbors.append(point)

        return neighbors
