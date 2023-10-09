import matplotlib.pyplot as plt
import seaborn as sns 

# customize the plots
plt.rcParams['figure.figsize'] = [12, 6]
sns.set(style='dark')
sns.set(rc={'figure.dpi': 300})
sns.set(font='monospace')
sns.despine(left=True, right=True, top=True, bottom=True)
cmap_color=sns.color_palette("Blues", as_cmap=True)


def distribution_plots(data, title, x_label, y_label, bins=None):
    """
    Plots the distribution of the given data.

    Parameters:
    data (pandas.Series): The data to plot.
    title (str): The title of the plot.
    x_label (str): The label for the x-axis.
    y_label (str): The label for the y-axis.
    bins (int): The number of bins to use in the histogram.

    Returns:
    None
    """
    # plot the distribution 
    ax = plt.hist(data, bins=bins)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # calculate the min, max and average
    min_data = data.min()
    max_data = data.max()
    avg_data = data.mean()

    # plot the vertical lines to represent the min, max and avg sales
    plt.axvline(min_data, color='r', linestyle='--', label=f'Minimum: {min_data}')
    plt.axvline(max_data, color='g', linestyle='--', label=f'Maximum: {max_data}')
    plt.axvline(avg_data, color='k', linestyle='--', label=f'Average: {avg_data:,.2f}')
    plt.legend();

def monthly_averages_plots(data, attribute, ylabel, title):
    """
    Plots monthly averages of a specified attribute.

    Parameters:
    - data (pandas.DataFrame): The dataframe containing the time series data.
    - attribute (str): The name of the attribute/column for which monthly averages will be calculated and plotted.
    - ylabel (str): The label for the y-axis on the plot.
    - title (str): The title of the plot.

    Returns:
    None
    """
    ax = data[attribute].resample('M').mean().plot(ylabel=ylabel, title=title)
    ax.axhline(y=data[attribute].mean(), color='r')
    ax.legend([attribute + ' (mean=' + str(round(data[attribute].mean(), 2)) + ')'])
    ax.annotate('max', xy=(data[attribute].idxmax(), data[attribute].max()), xytext=(data[attribute].idxmax(), data[attribute].max() + 5), arrowprops=dict(facecolor='black', shrink=0.05))
    ax.annotate('min', xy=(data[attribute].idxmin(), data[attribute].min()), xytext=(data[attribute].idxmin(), data[attribute].min() - 5), arrowprops=dict(facecolor='black', shrink=0.05))


def heatmap_plots(dataframe, x_axis, y_axis, z_axis, aggfunc,title):
    """
    This function generates a heatmap for a given dataframe and columns.

    Parameters:
    dataframe (pandas.DataFrame): The dataframe containing the data to be analyzed.
    x_axis (str): The name of the column to be used as the x-axis.
    y_axis (str): The name of the column to be used as the y-axis.
    z_axis (str): The name of the column to be used as the z-axis.
    aggfunc (str): The aggregation function to be used while grouping.

    Returns:
    None
    """
    grouped = dataframe.groupby([x_axis, y_axis])[[z_axis]].agg(aggfunc).reset_index()
    pivoted = grouped.pivot_table(
        index=x_axis, columns=y_axis, values=z_axis
    )
    sns.heatmap(pivoted, cmap=cmap_color, annot=True, fmt='.0f')
    plt.xlabel('')
    plt.ylabel('')
    plt.title(title);

def horizontal_bar_plots(dataframe, x_col, y_col, title):
    """
    Plots a horizontal bar chart for the given dataframe with percentages.

    Parameters:
    dataframe (pandas.DataFrame): The dataframe containing the data to be plotted.
    x_col (str): The column name to be used as the x-axis.
    y_col (str): The column name to be used as the y-axis.
    title (str): The title of the plot.

    Returns:
    None
    """
    grouped_sales_by_market = dataframe.groupby(x_col)[[y_col]].sum().sort_values(by=y_col).reset_index()
    grouped_sales_by_market['percent'] = round((grouped_sales_by_market[y_col] / grouped_sales_by_market[y_col].sum()) * 100, 2)
    ax = grouped_sales_by_market.plot(kind='barh', x=x_col, y='percent', title=title, legend=False)
    
    # Add percentage labels
    for container in ax.containers:
        ax.bar_label(container, labels=[f'{val:.1f}%' for val in container.datavalues])
    plt.ylabel('');
