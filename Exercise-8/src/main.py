import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy


def calc_statistics(data_frame, param):
    # Calculate the median
    param_median = np.median(data_frame[param])
    print("Median of ", param, ': ', param_median)

    # Calculate the mode
    param_mode = scipy.stats.mode(data_frame[param])[0]
    print("Mode of ", param, ": ", param_mode)

    # Calculate the standard deviation
    param_standard_deviation = np.std(data_frame[param])
    print("Standard deviation of ", param, ": ", param_standard_deviation)

    # Calculate the variance of the temperature data
    param_variance = np.var(data_frame[param])
    print("Variance of ", param, ": ", param_variance)

    # Calculate the first quartile of the temperature data
    param_first_quartile = np.percentile(data_frame[param], 25)
    print("First quartile of ", param, ": ", param_first_quartile)

    # Calculate the third quartile of the temperature data
    param_third_quartile = np.percentile(data_frame[param], 75)
    print("Third quartile of ", param, ": ", param_third_quartile)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Load the data from the CSV file
    df = pd.read_csv("./data/complete_weather_data.csv")
    df.dropna(inplace=True)
    df = df.select_dtypes(include=[np.number])
    df.drop('index', axis=1, inplace=True)

    # Calculate descriptive statistics for each column
    print(df.describe())

    columns = list(df.columns)

    try:
        os.makedirs('./stats', exist_ok=True)
    except OSError as error:
        print("folder stats already exists!")

    try:
        os.makedirs('./stats/scatters', exist_ok=True)
    except OSError as error:
        print("folder scatters already exists!")

    try:
        os.makedirs('./stats/boxplots', exist_ok=True)
    except OSError as error:
        print("folder boxplots already exists!")

    # Create histograms for each column
    df.hist()
    plt.savefig("./stats/histograms", bbox_inches="tight",
                pad_inches=0.3, transparent=True)

    print('\n')
    for co1 in columns:
        columns_temp = columns.copy()
        columns_temp.remove(co1)
        calc_statistics(df, co1)
        for co2 in columns_temp:
            if co1 != 'hour':
                df.boxplot(by=co2, column=[co1], grid=False)
                plt.savefig('./stats/boxplots/' + co1 + '_' + co2, bbox_inches="tight",
                            pad_inches=0.3, transparent=True)
            if co2 != 'hour':
                df.plot.scatter(x=co1, y=co2)
                plt.savefig('./stats/scatters/' + co1 + '_' + co2, bbox_inches="tight",
                            pad_inches=0.3, transparent=True)


    df.drop('hour', axis=1, inplace=True)

    # Create box plots for each column
    df.boxplot()
    plt.savefig('./stats/boxplot', bbox_inches="tight",
                pad_inches=0.3, transparent=True)
    # Obtain and draw the correlation matrix
    correlation_matrix = df.corr()
    sns.heatmap(correlation_matrix, annot=True)
    plt.savefig('./stats/correlation_matrix', bbox_inches="tight",
                pad_inches=0.3, transparent=True)
