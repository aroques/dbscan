import numpy


# http://mccormickml.com/2016/11/08/dbscan-clustering/

class DBScan:
    def __init__(self, min_points, epsilon):
        self.min_points = min_points
        self.epsilon = epsilon
        self.point_labels = None
        self.cluster_labels = None

    def fit(self, data):
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

    def region_query(self, data, point):
        neighbors = []

        for Pn in range(0, len(data)):

            if numpy.linalg.norm(data[point] - data[Pn]) < self.epsilon:
                neighbors.append(Pn)

        return neighbors

# def get_connected_core_point_graph(core_points, data, neighborhoods):
#     core_point_graph = defaultdict(list)
#     for i, core_point in enumerate(core_points):
#         neighborhood = get_neighborhood(core_point, data, neighborhoods)
#         for point in neighborhood:
#             if point not in core_points or point == core_point:
#                 continue
#             # Point is a core point that is not itself
#             j = core_points.index(point)
#             # Add core point to neighborhood of this core point
#             core_point_graph[i].append(j)
#
#     return core_point_graph
#
#
# def get_neighborhood(core_point, data, neighborhoods):
#     i = data.index(core_point)
#     neighborhood = neighborhoods[i]
#     return neighborhood
#
#
# def in_neighborhood_of_core_point(labels, neighborhoods, unlabeled_point) -> bool:
#     """Check if unlabeled point is in the neighborhood of a core point.
#
#     Args:
#         labels: List of labels that correspond to each point in a dataset: 'core', 'border', or 'noise'.
#         neighborhoods: List of points that are in the neighborhood of each point.
#         unlabeled_point: A point that is either a noise or border point.
#
#     Returns:
#         Whether or not the unlabeled point is in the neighborhood of a core point.
#
#     """
#     for j, label in enumerate(labels):
#         if label == 'core' and unlabeled_point in neighborhoods[j]:
#             # Unlabeled point is in neighborhood of a core point
#             return True
#     return False
#
#
# def get_core_points(data, point_labels):
#     core_points = []
#     for i, label in enumerate(point_labels):
#         if label != 'core':
#             continue
#         core_points.append(data[i])
#     return core_points
# def label_border_and_noise_points(data, labels, neighborhoods):
#     """Labels borders and noise points.
#
#     Args:
#         data: A dataset.
#         labels: A list of labels that correspond to each point in the dataset.
#         neighborhoods: List of points that are in the neighborhood of each point.
#
#     Returns:
#         A list of labels that correspond to each point in a dataset: 'core', 'border', or 'noise'.
#
#     """
#     for i, this_label in enumerate(labels):
#         if this_label != 'border or noise':
#             continue  # Core point so continue
#         unlabeled_point = data[i]
#         if in_neighborhood_of_core_point(labels, neighborhoods, unlabeled_point):
#             labels[i] = 'border'
#         else:
#             labels[i] = 'noise'
#
#     return labels
# def __get_cluster_labels(self, core_points: List[List], data: List[List], neighborhoods: List[List]) -> List[int]:
#     cluster_labels = [-1 for _ in range(len(data))]
#     num_clusters = -1
#     for core_point in core_points:
#         index = data.index(core_point)
#
#         if cluster_labels[index] == -1:
#             num_clusters += 1
#             cluster_labels[index] = num_clusters
#
#         current_cluster_label = cluster_labels[index]
#
#         neighborhood = neighborhoods[index]
#
#         cluster_labels = self.__label_points_in_neighborhood(cluster_labels, core_point,
#                                                              current_cluster_label, data, neighborhood)
#
#     return cluster_labels
#
# @staticmethod
# def __label_points_in_neighborhood(cluster_labels, core_point, current_cluster_label, data, neighborhood):
#     for point in neighborhood:
#         if point == core_point:
#             continue
#         index = data.index(point)
#         if cluster_labels[index] == -1:
#             cluster_labels[index] = current_cluster_label
#     return cluster_labels
#
# def __label_core_points(self, neighborhoods: List[List]) -> List[str]:
#     """Labels all core points.
#
#     Args:
#         neighborhoods: List of points that are in the neighborhood of each point.
#
#     Returns:
#         A list of labels that correspond to each point in the dataset.
#
#     """
#     labels = []
#     for i, neighborhood in enumerate(neighborhoods):
#         if len(neighborhood) >= (self.min_points - 1):
#             labels.append('core')
#         else:
#             labels.append('border or noise')
#     return labels
#
# def __get_neighborhoods(self, data: List[List]) -> List[List]:
#     """Gets a list of the points that are in the neighborhood of each point.
#
#     Args:
#         data: A dataset.
#
#     Returns:
#         A list of points that are in the neighborhood of each point.
#
#     """
#     neighborhoods = []
#     for point in data:
#         points_in_neighborhood = self.__get_points_in_neighborhood(data, point)
#         neighborhoods.append(points_in_neighborhood)
#     return neighborhoods
#
# def __get_points_in_neighborhood(self, data, this_point):
#     """Get a list of points that are in the neighborhood of this_point.
#
#     Args:
#         data: A dataset.
#         this_point: A data point.
#
#     Returns:
#         A list of points that are in the neighborhood of this_point.
#
#     """
#     points_in_neighborhood = []
#     for point in data:
#         if this_point == point:
#             continue
#         distance = euclidean(this_point, point)
#         if distance < self.epsilon:
#             points_in_neighborhood.append(point)
#     return points_in_neighborhood
#
# def get_points_for_plotting(self, data):
#     core_points = []
#     border_points = []
#     noise_points = []
#     for i, label in enumerate(self.point_labels):
#         if label == 'core':
#             core_points.append(data[i])
#         elif label == 'border':
#             border_points.append(data[i])
#         elif label == 'noise':
#             noise_points.append(data[i])
#     return core_points, border_points, noise_points
