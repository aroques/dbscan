from dataviz import plot_data, get_datasets


def main():
    datasets = get_datasets()
    for dataset in datasets:
        plot_data(dataset)


if __name__ == '__main__':
    main()
