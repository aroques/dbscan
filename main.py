from dataviz import plot_data, get_datasets, plot_labeled_data
from dbscan import DBScan, get_kdist_data


def main():
    datasets = get_datasets()

    min_points = 5
    eps = [18, 17, 10, 5]

    for i, dataset in enumerate(datasets):
        pass
        # Plot kdist plot to determine EPS param
        # kdist_data = get_kdist_data(dataset, min_points)
        # plot_data(kdist_data)

        # Get dbscan object
        # dbscan = DBScan(min_points, eps[i])
        # dbscan.fit(dataset)
        # cpts, bpts, npts = dbscan.get_points_for_plotting(dataset)

        # plot_data(cpts)
        # plot_data(bpts)
        # plot_data(npts)
        #
        # plot_labeled_data(dataset, dbscan.cluster_labels)

    ds = datasets[3]
    dbscan = DBScan(min_points, eps[3])
    dbscan.fit(ds)
    cpts, bpts, npts = dbscan.get_points_for_plotting(ds)


if __name__ == '__main__':
    main()
