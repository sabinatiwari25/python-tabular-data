#! /usr/bin/env python3

"""
Perform linear regression and create scatter plots with regression lines
for each category in a tabular CSV file.
"""

import os
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def compose_plot_file_name(x_label, y_label, category_label = None):
    """
    Creates a name for a plot file based on the labels for the X, Y, and
    categorical variables.

    Parameters
    ----------
    x_label : str 
        The label for the X variable

    y_label : str 
        The label for the Y variable

    category_label : str 
        The label for the categorical variable. 

    Returns
    -------
    str
        The file name.
    """
    category_str = ""
    if category_label:
        category_str = "-by-{0}".format(category_label)
    plot_path = "{0}-v-{1}{2}.pdf".format(x_label, y_label,
            category_str)
    return plot_path

def regress_and_scatter(dataframe, x_column_name, y_column_name,
        category_column_name = None,
        plot_path = None):
    """
    Generates a scatter plot from the data in the pandas DataFrame,
    `dataframe`.

    Each occurence of `target_regex` is written to a new line, and the line
    number and string are separated by a tab ('\t') character.

    Parameters
    ----------
    dataframe : A pandas DataFrame
        The columns for this dataframe (see below) will be used for plotting.

    x_column_name : str 
        The name of the column in `dataframe` to plot along the X-axis
        and treat as the predictor variable in the regression.

    y_column_name : str 
        The name of the column in `dataframe` to plot along the Y-axis
        and treat as the response variable in the regression.

    category_column_name : str 
        The name of the column in `dataframe` to use as a categorical variable.
        If provided, the `dataframe` is broken up by rows using this variable
        and analyzed separately. If not provided, all of the rows of the
        `dataframe` are analyzed together.

    plot_path : str
        The path where the plot will be saved. If not provided, the plot will
        be saved to the current working directory and the name will be based on
        the X, Y, and category column names.
        

    Returns
    -------
    None
        The plot is saved and nothing is returned.
    """
    # If no plot path is provided, we will save the plot to the current working
    # directory and use the x and y column names for the file name
    if not plot_path:
        plot_path = compose_plot_file_name(x_column_name, y_column_name,
                category_column_name)

    # Break up the dataframe into groups based on the columm with the
    # categorical variable
    if category_column_name:
        grouped_dataframes = dataframe.groupby(category_column_name)
    else:
        # If no category column was provided we will plot all the data at once,
        # but we need to put the dataframe in a tuple of tuples so that the
        # `for` loop below will work
        grouped_dataframes = ('all', dataframe),

    # Get the min and max values of X to use for the regression lines
    # below
    x_min = min(dataframe[x_column_name])
    x_max = max(dataframe[x_column_name])

    # Loop over our grouped dataframes and plot the points and regression line
    color_index = 0
    for category, df in grouped_dataframes:
        x = df[x_column_name]
        y = df[y_column_name]
        regression = stats.linregress(x, y)
        slope = regression.slope
        intercept = regression.intercept
        plt.scatter(x, y, label = category, color = 'C' + str(color_index))

        # Get Y values predicted by linear regression for the min and max X
        # vlaues
        y1 = slope * x_min + intercept
        y2 = slope * x_max + intercept
        # Plot the regression line
        plt.plot((x_min, x_max), (y1, y2),
                color = 'C' + str(color_index))
        color_index += 1

    # Add labels and legend and save the plot
    plt.xlabel(x_column_name)
    plt.ylabel(y_column_name)
    plt.legend()
    plt.savefig(plot_path)

