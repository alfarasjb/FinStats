import pandas as pd 
import numpy as np
import yfinance as yf
import math 
import scipy.stats as sc
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates 
import seaborn as sns

plt.style.use('seaborn-darkgrid')

class Calc:

    def __init__(self, symbol: str, samples: int):
        self.symbol = symbol
        self.samples = samples 

    @property
    def symbol(self):
        return self._symbol 

    @property
    def samples(self):
        return self._samples 
    
    @symbol.setter 
    def symbol(self, symbol):
        self._symbol = symbol 
    
    @samples.setter
    def samples(self, samples):
        self._samples = samples

    def download(self):

        df = yf.download(self.symbol, interval = '1d').tail(self.samples)
        if df.empty:
            raise ValueError(f'No data for symbol: {self.symbol}')
        
        return df

    def build_data(self):
        # return to event handler
        assert self.samples > 5
        try: 
            df = self.download()
            close = df['Close']
            mean, median, mode = np.mean(close), np.median(close), sc.mode(close, keepdims = True)
            var, skew, kurt, sdev = np.var(close), sc.skew(close), sc.kurtosis(close), math.sqrt(np.var(close))
            start_date = df.index[0].strftime('%m/%d/%Y')
            end_date = df.index[-1].strftime('%m/%d/%Y')
            main_data = [self.samples, start_date, end_date, mean, median.item(), mode[0][0].item(), sdev, var, skew, kurt]
            updated = [round(d, 2) if type(d) == float else d for d in main_data]
            key = ['samples','start','end','mean','median','mode','sdev','var','skew','kurt']
            self.data = {k:v for k,v in zip(key,updated)}
            self.close = close 
            return self.data, self.close

        except ValueError:
            return None, None
    
        
    def plot_data(self):
        samples = self.data['samples']
        mean = self.data['mean']
        sdev = self.data['sdev']
        var = self.data['var']
        skew = self.data['skew']
        kurt = self.data['kurt']
        
        close_label = f'Close - {self.symbol} | {samples} days'
        fs = 8
        fc = '#EAEAF2'
        fig_w, fig_h = 5, 4.2

        # hist portion
        hist, axh = plt.subplots(facecolor = fc, edgecolor = 'black')
        hist.set_size_inches(fig_w, fig_h)
        axh.clear()
        axh = sns.distplot(self.close, kde = True, bins = 10)
        axh.axvline(mean, ls = '--', label = f'Mean {mean}')
        axh.axvline(mean + sdev, ls = ':', label = f'Std. Dev +/- {sdev}')
        axh.axvline(mean - sdev, ls = ':')
        axh.set_ylabel('Density', fontsize = fs)
        axh.set_xlabel(close_label, fontsize = fs)
        axh.tick_params(labelsize = fs)
        axh.axes.set_title(f'Variance: {var} | Skew: {skew} | Kurt: {kurt}', fontsize = fs)
        axh.legend(fontsize = fs)

        # price portion
        interval = round(int(samples) / 5)
        pc, axp = plt.subplots(facecolor = fc, edgecolor = 'black')
        pc.set_size_inches(fig_w, fig_h)
        axp.clear()
        plt.plot(self.close, label = 'Close')
        plt.ylabel(close_label, fontsize = fs)
        plt.xlabel('Date', fontsize = fs)
        plt.xticks(fontsize = fs, rotation = 45)
        plt.yticks(fontsize = fs)
        plt.legend(fontsize = fs)
        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.DayLocator(interval = interval))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        plt.gcf().autofmt_xdate()

        return hist, pc