import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

NUM_PRICE_COLUMNS_YAHOO_FINANCE = 6
INDEX_OF_DATE_COLUMN_YAHOO_FINANCE = 0

""" Data class assumes stock history downloaded from Yahoo Finance"""


class Data:
    def __init__(self, filename, date_col=INDEX_OF_DATE_COLUMN_YAHOO_FINANCE,
                 price_col=NUM_PRICE_COLUMNS_YAHOO_FINANCE):
        self._fn = filename
        self._date_col = date_col
        self._price_col = price_col
        self._data = None
        self._model = None

    def to_panda(self, name, remove_nan=True):
        """
        We added nan for that last entry but usually do not need it so by default we do not return it.
        """
        raw = pd.read_csv(self._fn, sep=',', usecols=[self._date_col, self._price_col], names=['Date', 'Price'],
                          header=0)
        raw = raw.rename(columns={'Price': name + '_price', 'Returns': name + '_returns'})

        # Convert Prices to returns: ( y[i]/y[i-1]) ) - 1
        returns = np.array(raw[name + '_price'][:-1], np.float) / np.array(raw[name + '_price'][1:], np.float) - 1

        # append with NAN
        raw[name + '_returns'] = np.append(returns, np.nan)
        raw.index = raw['Date']

        # Remove the Date column
        self._data = raw.drop(['Date'], axis=1)
        return self._data[:-1] if remove_nan else self._data


class DataTool:
    def __init__(self, data_aggregate):
        self._data_aggregate = data_aggregate

    def corr_matrix(self, out_dir, vmax=0.8, figure_size=(12, 9)):
        """
        correlation matrix
        The higher the correlation of a feature with Independent Varibale, the more important that feature is in prediction
        :param out_dir:
        :data_aggreagte: dataframe with all data(y and X)
        :param vmax:
        :param figure_size:
        :param zoom: If set True we only show the heat map for the variables set by num_var
        :param num_var:
        :return:
        """
        correlation_matrix = self._data_aggregate.corr()
        sns.heatmap(correlation_matrix, vmax=vmax, square=True)
        plt.savefig(out_dir+'/corr_matrix.png')
