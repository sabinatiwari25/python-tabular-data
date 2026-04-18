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
        Output plot file name.
    """
        safe_species = species_name.replace(" ", "_")
        return f"{safe_species}_{x_label}_vs_{y_label}.png"

    def plot_regression(dataframe, x_column_name, y_column_name, species_name, output_dir):
    """
    Create a scatter plot and regression line for one species.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Data for one species only.
    x_column_name : str
        Name of the predictor column.
    y_column_name : str
        Name of the response column.
    species_name : str
        Name of the species being plotted.
    output_dir : str
        Directory where the plot file will be saved.

    Returns
    -------
    str
        Path to the saved plot.
    """
    x = dataframe[x_column_name]
    y = dataframe[y_column_name]

    regression = stats.linregress(x, y)
    slope = regression.slope
    intercept = regression.intercept

    x_min = x.min()
    x_max = x.max()
    y_min = slope * x_min + intercept
    y_max = slope * x_max + intercept

    plt.figure()
    plt.scatter(x, y, label="Data")
    plt.plot([x_min, x_max], [y_min, y_max], label="Regression line")
    plt.xlabel(x_column_name)
    plt.ylabel(y_column_name)
    plt.title(f"{species_name}: {y_column_name} vs {x_column_name}")
    plt.legend()

    file_name = compose_plot_file_name(species_name, x_column_name, y_column_name)
    plot_path = os.path.join(output_dir, file_name)
    plt.savefig(plot_path)
    plt.close()

    return plot_path

    def regress_and_plot_by_species(dataframe, x_column_name, y_column_name, category_column_name, output_dir):
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
    output_dir : str
        Directory where plots will be saved.

    Returns
    -------
    list of str
        Paths to the saved plot files.
    """
    saved_plots = []

    for species_name, species_df in dataframe.groupby(category_column_name):
        plot_path = plot_regression(
            species_df,
            x_column_name,
            y_column_name,
            species_name,
            output_dir
        )
        saved_plots.append(plot_path)

    return saved_plots


    def main_cli():
    """
    Run the command-line interface for the script.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "path",
        type=str,
        help="Path to the CSV file."
    )
    parser.add_argument(
        "-x", "--x",
        type=str,
        default="petal_length_cm",
        help="Column name to plot on the x-axis."
    )
    parser.add_argument(
        "-y", "--y",
        type=str,
        default="sepal_length_cm",
        help="Column name to plot on the y-axis."
    )
    parser.add_argument(
        "-c", "--category",
        type=str,
        default="species",
        help="Column name to use as the categorical grouping variable."
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=".",
        help="Directory where plots will be saved."
    )

    args = parser.parse_args()

    if not os.path.exists(args.path):
        sys.exit(f"ERROR: The path {args.path} does not exist.")

    if not os.path.isfile(args.path):
        sys.exit(f"ERROR: The path {args.path} is not a file.")

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    try:
        dataframe = pd.read_csv(args.path)
    except Exception as error:
        sys.stderr.write(f"ERROR: Could not read {args.path}\n")
        raise error

    for column_name in [args.x, args.y, args.category]:
        if column_name not in dataframe.columns:
            sys.exit(f"ERROR: Column '{column_name}' not found in the CSV file.")

    saved_plots = regress_and_plot_by_species(
        dataframe,
        args.x,
        args.y,
        args.category,
        args.output_dir
    )

    for plot_path in saved_plots:
        print(f"Saved plot: {plot_path}")


if __name__ == "__main__":
    main_cli()
