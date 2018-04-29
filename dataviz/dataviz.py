from typing import List
from random import Random
from collections import defaultdict
from itertools import chain
import csv
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_labeled_data(data: List[List], labels: List[int]) -> None:
    """Plot labeled data.

    Args:
        data: Data to plot.
        labels: The cluster each point belongs to.

    Returns:
        None
    """

    # Setup needed to construct plot
    num_labels = len(set(labels))
    markers = get_markers(num_labels)
    palette = get_palette(num_labels)
    columns = ['x', 'y']

    # Get dataframe for data
    df = pd.DataFrame(data, columns=columns)
    df['labels'] = pd.Series(labels, index=df.index)  # Add labels as a column for coloring

    # Plot
    sns.lmplot(*columns, data=df, fit_reg=False, legend=False,
               hue='labels', palette=palette, markers=markers,
               scatter_kws={'s': 50})
    plt.show()


def plot_data(data: List[List]) -> None:
    """Plot data.

    Args:
        data: Data to plot.

    Returns:
        None
    """

    # Setup needed to construct plot
    columns = ['x', 'y']

    # Get dataframe for data
    df = pd.DataFrame(data, columns=columns)

    size_of_point = 35

    # Plot
    sns.lmplot(*columns, data=df, fit_reg=False, legend=False, scatter_kws={'s': size_of_point})
    plt.show()


def get_markers(num_markers):
    random = Random(0)
    markers = ['*', 'o', '^', '+']
    markers = random.choices(population=markers, k=num_markers)
    return markers


def get_palette(num_colors):
    random = Random(0)
    colors = ['blue', 'orange', 'green', 'purple', 'red']
    colors = random.choices(population=colors, k=num_colors)
    colors.append('red')
    return colors


def get_datasets() -> List:
    """Uses dataset parameters from a csv file to produces n datasets.

    Returns:
        N datasets.

    """
    datasets = defaultdict(list)
    with open('dataviz/dataset_parameters.csv', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # Parse the row for dataset parameters
            id = int(row['dataset id'])
            number_of_points = int(row['number of points'])
            bounds_for_x = [float(x.strip()) for x in row['bounds for x'].split(',')]
            bounds_for_y = [float(x.strip()) for x in row['bounds for y'].split(',')]
            seed = int(row['seed'])

            # Pass parameters in to get some data
            data = generate_random_points(number_of_points, bounds_for_x, bounds_for_y, seed)

            # Add data to the dataset it belongs to
            datasets[id].append(data)

    return flatten_datasets(datasets)


def flatten_datasets(datasets: defaultdict) -> list:
    """Concatenates together 'sub datasets' into one dataset

    A 'sub dataset' could be one 'square' of data

    Args:
        datasets: A default dictionary of datasets

    Returns:
        A list of datasets

    """
    flattened_datasets = []
    for dataset in datasets.values():
        flattened_dataset = list(chain.from_iterable(dataset))
        flattened_datasets.append(flattened_dataset)
    return flattened_datasets


def generate_random_points(num_points: int, bound_for_x: List[float], bound_for_y: List[float], seed: int):
    """Generate random data.

    Args:
        num_points: The number of points to generate.
        bound_for_x: The bounds for possible values of X.
        bound_for_y: The bounds for possible values of Y.
        seed: Seed for Random.

    Returns:
        N points
    """
    r = Random(seed)
    x_min, x_max = bound_for_x
    y_min, y_max = bound_for_y
    data = []
    for _ in range(num_points):
        x = x_min + (x_max - x_min) * r.random()
        y = y_min + (y_max - y_min) * r.random()
        point = (x, y)
        data.append(point)
    return data
