import pandas as pd
import numpy as np
import scipy.stats as sc
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
import seaborn as sns 


plt.style.use('seaborn-darkgrid')


class Stat_Info():


    def __init__(self, symbol: str, sample_size: int):

        if int(sample_size) < 5:
            raise ValueError('Invalid Sample Size {sample_size}')
        
        self.symbol = symbol 
        self.sample_size = sample_size 

    @property
    def symbol(self):
        return self._symbol 
    
    @property
    def sample_size(self):
        return self._sample_size

    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol 

    @sample_size.setter
    def sample_size(self, sample_size):
        self._sample_size = sample_size


    def download(self):
        # download yf data
        # check for sample size validity - raise value error if negative
        # overwrite any existing df 

        df = yf.download(self.symbol, interval = '1d').tail(self.sample_size)
        if df.empty:
            raise ValueError(f'No data for symbol: {self.symbol}')
        return df
    
    def build_data(self):
        # construct df and calculate stat metrics
        df = self.download()
        close = df['Close']
        mean, median, mode = np.mean(close), np.median(close), sc.mode(close, keepdims = True)
        var, skew, kurt, sdev = np.var(close), sc.skew(close), sc.kurtosis(close), math.sqrt(np.var(close))
        start_date = df.index[0].strftime('%m/%d/%Y')
        end_date = df.index[-1].strftime('%m/%d/%Y')
        main_data = [self.sample_size, start_date, end_date, mean, median.item(), mode[0][0].item(), sdev, var, skew, kurt]
        updated = []

        for data in main_data:
            if type(data) == float:
                data = round(data, 2)
            updated.append(data) 

        self.close = close

        return updated, close          


    def plot_data(self, type: str = 'hist'):
        # plot data: hist or price
        title = f'{self.symbol} | {self.sample_size} days'
        fig, ax = plt.subplots(facecolor = '#EAEAF2', edgecolor = 'black')
        fig.set_size_inches(5, 3.8)
        ax.clear()

        if type == 'hist':
            ax = sns.distplot(self.close, kde = True, bins = 10)
            ax.set_ylabel('Density', fontsize = 8)
            ax.set_xlabel('Close', fontsize = 8)
            ax.axes.set_title(title)
            ax.tick_params(labelsize = 8)

        elif type == 'price':
            interval = round(self.sample_size / 5)
            plt.plot(self.close)
            plt.title(title)
            plt.ylabel('Close', fontsize = 10)
            plt.xlabel('Date', fontsize = 10)
            plt.xticks(fontsize = 8, rotation = 45)
            plt.yticks(fontsize = 8)
            ax = plt.gca()
            ax.xaxis.set_major_locator(mdates.DayLocator(interval = interval))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            plt.gcf().autofmt_xdate()

        return fig


if __name__ == "__main__":
    l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    multiplied = [l**2 if l%2 == 0 else l for l in l1]
    print(multiplied)