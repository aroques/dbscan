from collections import defaultdict
from typing import List
from random import Random
import csv
from itertools import chain


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
