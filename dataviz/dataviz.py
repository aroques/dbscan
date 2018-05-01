from typing import List
from random import Random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_labeled_data(data: List[List], labels: List[int]) -> None:
    """Plot labeled data.

    Args:
        data: Data to plot.
        labels: The cluster each point belongs to.
        core_points: core points

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

    # # Add core points to dataframe
    # corepoints_df = pd.DataFrame(core_points, columns=columns)
    # corepoints_df['labels'] = ['centroid' for _ in range(len(corepoints_df))]
    # df = df.append(corepoints_df, ignore_index=True)

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
    markers = ['*', 'o', '^', '+', 's', 'p', 'D', '8', '<', '>', '1', '2', '3', 'h', 'H', 'x', 'v', '_', 'd', ',']
    markers = random.population(population=markers, k=num_markers)
    return markers


def get_palette(num_colors):
    random = Random(0)
    colors = ['blue', 'orange', 'green', 'purple', 'brown', 'black', 'pink', 'magenta', 'gray',
              'lime', 'teal', 'navy', 'plum', 'olive', 'fuchsia', 'red']
    colors = random.sample(population=colors, k=num_colors)
    return colors


