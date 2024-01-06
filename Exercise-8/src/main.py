import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy
from tqdm import tqdm


class DataAnalysis:
    def __init__(self, base_path):
        self.base_path = base_path
        self.df = None
        self.results_file = f'{self.base_path}/analysis_results.txt'
        self.results_content = []

    def load_data(self, file_path):
        self.df = pd.read_csv(file_path)
        self.df.dropna(inplace=True)
        self.df = self.df.select_dtypes(include=[np.number])
        self.df.drop('index', axis=1, inplace=True)

    def create_directories(self, paths):
        for p in paths:
            try:
                os.makedirs(f'{self.base_path}{p}')
            except OSError as error:
                print("Folder " + p.split('/')[-1] + " already exists!")

    def write_to_file(self, content):
        self.results_content.append(content)

    def close_file(self):
        with open(self.results_file, 'a') as file:
            for content in self.results_content:
                file.write(content + '\n')

    def calc_statistics(self, param):
        param_median = np.median(self.df[param])
        self.write_to_file(f"Median of {param}: {param_median}")

        param_mode = scipy.stats.mode(self.df[param])[0]
        self.write_to_file(f"Mode of {param}: {param_mode}")

        param_standard_deviation = np.std(self.df[param])
        self.write_to_file(f"Standard deviation of {param}: {param_standard_deviation}")

        param_variance = np.var(self.df[param])
        self.write_to_file(f"Variance of {param}: {param_variance}")

        param_first_quartile = np.percentile(self.df[param], 25)
        self.write_to_file(f"First quartile of {param}: {param_first_quartile}")

        param_third_quartile = np.percentile(self.df[param], 75)
        self.write_to_file(f"Third quartile of {param}: {param_third_quartile}")

    def save_boxplot(self, current_column):
        self.df.plot.box(column=current_column, color={'whiskers': 'black',
                                                       'caps': 'black',
                                                       'medians': 'black',
                                                       'boxes': 'black'})
        plt.savefig(f'{self.base_path}/stats/boxplot_by_column/{current_column}')

    def analyze_data(self):
        self.create_directories(['/stats', '/stats/scatters', '/stats/boxplots', '/stats/boxplot_by_column'])
        self.write_to_file(str(self.df.describe()) + '\n')

        columns = list(self.df.columns)
        for co1 in tqdm(columns, desc="Analyzing Data", unit="column", colour='green',
                        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"):
            self.save_boxplot(co1)
            columns_temp = columns.copy()
            columns_temp.remove(co1)
            self.calc_statistics(co1)
            for co2 in columns_temp:
                if co1 != 'hour':
                    self.df.boxplot(by=co2, column=[co1], grid=False)
                    plt.savefig(f'{self.base_path}/stats/boxplots/{co1}_{co2}', bbox_inches="tight",
                                pad_inches=0.3, transparent=True)
                if co2 != 'hour':
                    self.df.plot.scatter(x=co1, y=co2)
                    plt.savefig(f'{self.base_path}/stats/scatters/{co1}_{co2}',
                                bbox_inches="tight", pad_inches=0.3, transparent=True)
                plt.close()

        self.df.drop('hour', axis=1, inplace=True)

        self.df.hist()
        plt.savefig(f'{self.base_path}/stats/histograms',
                    bbox_inches="tight", pad_inches=0.3, transparent=True)
        plt.close()

        correlation_matrix = self.df.corr()
        sns.heatmap(correlation_matrix, annot=True)
        plt.savefig(f'{self.base_path}/stats/correlation_matrix',
                    bbox_inches="tight", pad_inches=0.3, transparent=True)
        plt.close()
        # Close the file after writing everything
        self.close_file()


if __name__ == '__main__':
    print("Calculating...!")
    base_path = '..'
    data_analysis = DataAnalysis(base_path)
    data_analysis.load_data(f'{base_path}/data/complete_weather_data.csv')
    data_analysis.analyze_data()
    print("Finished! Check the stats folder for plots and analysis_results.txt for outputs!")
