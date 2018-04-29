from typing import List
from scipy.spatial.distance import euclidean


class DBScan:
    def __init__(self, min_points, epsilon):
        self.min_points = min_points
        self.epsilon = epsilon
        self.point_labels = None
        self.cluster_labels = None

    def fit(self, data: List[List]) -> List:
        # Label all data as a core, border, or noise point
        neighborhoods = self.__get_neighborhoods(data)

        point_labels = self.__label_core_points(neighborhoods)
        self.point_labels = self.__label_border_and_noise_points(data, point_labels, neighborhoods)

        core_points = self.__get_core_points(data, point_labels)

        self.cluster_labels = self.__get_cluster_labels(core_points, data, neighborhoods)

    def __get_cluster_labels(self, core_points, data, neighborhoods):
        cluster_labels = [-1 for _ in range(len(data))]
        current_cluster_label = 0
        for core_point in core_points:
            index = data.index(core_point)
            if cluster_labels[index] == -1:
                current_cluster_label += 1
                cluster_labels[index] = current_cluster_label
            neighborhood = neighborhoods[index]
            cluster_labels = self.__label_points_in_neighborhood(cluster_labels, core_point,
                                                                 current_cluster_label, data, neighborhood)
        return cluster_labels

    @staticmethod
    def __label_points_in_neighborhood(cluster_labels, core_point, current_cluster_label, data, neighborhood):
        for point in neighborhood:
            if point == core_point:
                continue
            index = data.index(point)
            if cluster_labels[index] == -1:
                cluster_labels[index] = current_cluster_label
        return cluster_labels

    @staticmethod
    def __get_core_points(data, point_labels):
        core_points = []
        for i, label in enumerate(point_labels):
            if label != 'core':
                continue
            core_points.append(data[i])
        return core_points

    def __label_border_and_noise_points(self, data, labels, neighborhoods):
        """Labels borders and noise points.

        Args:
            data: A dataset.
            labels: A list of labels that correspond to each point in the dataset.
            neighborhoods: List of points that are in the neighborhood of each point.

        Returns:
            A list of labels that correspond to each point in a dataset: 'core', 'border', or 'noise'.

        """
        for i, this_label in enumerate(labels):
            if this_label != 'border or noise':
                continue  # Core point so continue
            unlabeled_point = data[i]
            if self.in_neighborhood_of_core_point(labels, neighborhoods, unlabeled_point):
                labels[i] = 'border'
            else:
                labels[i] = 'noise'

        return labels

    @staticmethod
    def in_neighborhood_of_core_point(labels, neighborhoods, unlabeled_point) -> bool:
        """Check if unlabeled point is in the neighborhood of a core point.

        Args:
            labels: List of labels that correspond to each point in a dataset: 'core', 'border', or 'noise'.
            neighborhoods: List of points that are in the neighborhood of each point.
            unlabeled_point: A point that is either a noise or border point.

        Returns:
            Whether or not the unlabeled point is in the neighborhood of a core point.

        """
        for j, label in enumerate(labels):
            if label == 'core' and unlabeled_point in neighborhoods[j]:
                # Unlabeled point is in neighborhood of a core point
                return True
        return False

    def __label_core_points(self, neighborhoods: List[List]) -> List[str]:
        """Labels all core points.

        Args:
            neighborhoods: List of points that are in the neighborhood of each point.

        Returns:
            A list of labels that correspond to each point in the dataset.

        """
        labels = []
        for i, neighborhood in enumerate(neighborhoods):
            if len(neighborhood) >= self.min_points:
                labels.append('core')
            else:
                labels.append('border or noise')
        return labels

    def __get_neighborhoods(self, data: List[List]) -> List[List]:
        """Gets a list of the points that are in the neighborhood of each point.

        Args:
            data: A dataset.

        Returns:
            A list of points that are in the neighborhood of each point.

        """
        neighborhoods = []
        for point in data:
            points_in_neighborhood = self.__get_points_in_neighborhood(data, point)
            neighborhoods.append(points_in_neighborhood)
        return neighborhoods

    def __get_points_in_neighborhood(self, data, this_point):
        """Get a list of points that are in the neighborhood of this_point.

        Args:
            data: A dataset.
            this_point: A data point.

        Returns:
            A list of points that are in the neighborhood of this_point.

        """
        points_in_neighborhood = []
        for point in data:
            if this_point == point:
                continue
            distance = euclidean(this_point, point)
            if distance < self.epsilon:
                points_in_neighborhood.append(point)
        return points_in_neighborhood
