from dataviz import plot_data, get_datasets, plot_labeled_data
from dbscan import DBScan, get_kdist_data


def main():
    datasets = get_datasets()

    min_points = 5
    eps = [18, 17, 10, 5]

    for i, dataset in enumerate(datasets):
        # Plot kdist plot to determine EPS param
        # kdist_data = get_kdist_data(dataset, min_points)
        # plot_data(kdist_data)

        # Get dbscan object
        dbscan = DBScan(min_points, eps[i])
        labels = dbscan.fit(dataset)
        print(labels)


if __name__ == '__main__':
    main()
