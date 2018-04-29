from dataviz import plot_data, get_datasets
from dbscan import DBScan, get_kdist_data


def main():
    datasets = get_datasets()

    min_points = 4
    eps = [17, 16, 8]

    for i, dataset in enumerate(datasets):
        # Plot kdist plot to determine EPS param
        kdist_data = get_kdist_data(dataset, min_points)
        plot_data(kdist_data)

        # Get dbscan object
        dbscan = DBScan(min_points, eps[i])


if __name__ == '__main__':
    main()
