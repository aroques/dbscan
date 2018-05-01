import numpy


#

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

            if not (labels[point] == 0):
                continue

            neighbor_points = self.region_query(data, point)

            if len(neighbor_points) < self.min_points:
                labels[point] = -1
            else:
                cluster_id += 1
                self.grow_cluster(data, labels, point, neighbor_points, cluster_id)

        return labels

    def grow_cluster(self, data, labels, point, neighbor_points, cluster_id):
        labels[point] = cluster_id

        i = 0
        while i < len(neighbor_points):

            neighbor_point = neighbor_points[i]

            if labels[neighbor_point] == -1:
                labels[neighbor_point] = cluster_id
            elif labels[neighbor_point] == 0:
                labels[neighbor_point] = cluster_id

                neighbor_point_neighborhood = self.region_query(data, neighbor_point)

                if len(neighbor_point_neighborhood) >= self.min_points:
                    neighbor_points = neighbor_points + neighbor_point_neighborhood
            i += 1

    def region_query(self, data, this_point):
        neighbors = []

        for point in range(0, len(data)):

            if numpy.linalg.norm(data[this_point] - data[point]) < self.epsilon:
                neighbors.append(point)

        return neighbors