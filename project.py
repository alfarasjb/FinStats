import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import warnings
from fpdf import FPDF
import os
from datetime import datetime as dt

## stats
import pandas as pd
import numpy as np
import scipy.stats as sc
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 
import math 
import seaborn as sns


warnings.filterwarnings('ignore')

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('green')
plt.style.use('seaborn-darkgrid')

title = 'Stocks in a nutshell'
w, h = 800, 550


class App(ctk.CTk):


    def __init__(self):
        super().__init__()

        self.cv, self.symbol, self.samples, self.data = None, None, None, None
        
        # WINDOW CONFIG
        self.title(title)
        self.geometry(f'{w}x{h}')
        self.maxsize(w, h)
        self.minsize(w, h)

        # Building UI
        self.build_parent_frames()
        self.build_main_header()
        self.build_input_fields()
        self.build_stats()
        self.build_tabview()

        
    def build_parent_frames(self):
        # header frame
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.place(relx = 0.02, rely = 0.025, relwidth = 0.96, relheight = 0.08)

        # data frame
        self.data_frame = ctk.CTkFrame(self, fg_color = 'transparent')
        self.data_frame.place(relx = 0.02, rely = 0.13, relwidth = 0.3, relheight = 0.85)

        # plot frame
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.place(relx = 0.34, rely = 0.13, relwidth = 0.64, relheight = 0.85)

    def build_tabview(self):
        # tabview
        tab_names = ['Histogram', 'Price']

        self.tabview = ctk.CTkTabview(self.plot_frame, command = self.tab_func)
        self.tabview.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        [self.tabview.add(tab_name) for tab_name in tab_names]

    def tab_func(self):
        
        name = self.tabview.get()
        master = self.tabview.tab(name)
        
        if self.cv is not None:
            self.cv.pack_forget()
        
        if name == 'Histogram':
            self.plot_fig(master, self.hist)
    
        elif name == 'Price':
            self.plot_fig(master, self.pc)
    
    def build_input_fields(self):

        # input fields: symbol and samples
        self.input_field_frame = ctk.CTkFrame(self.data_frame)
        self.input_field_frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.33)

        # row 
        master = self.input_field_frame
        self.symbol_name = ctk.CTkLabel(master, text = 'Ticker ID')
        self.symbol_entry = ctk.CTkEntry(master, placeholder_text = 'Symbol')
        self.sample_size = ctk.CTkLabel(master, text = 'Samples')
        self.sample_entry = ctk.CTkEntry(master, placeholder_text = 'Days')
        self.fetch_button = ctk.CTkButton(master, text = 'Fetch', command = self.fetch_data, width = 220)
        self.message = ctk.CTkLabel(master, text = '')

        self.symbol_name.grid(row = 0, column = 0, padx = (20, 5), pady = (15, 5))
        self.sample_size.grid(row = 1, column = 0, padx = (20, 5), pady = 5)
        self.symbol_entry.grid(row = 0, column = 1, padx = (5, 10), pady = (15, 5))
        self.sample_entry.grid(row = 1, column = 1, padx = (5, 10), pady = 5)
        self.fetch_button.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 5)
        self.message.grid(row = 3, column = 0, columnspan = 2, padx = 10, pady = 0)
        
    def export_data(self):
        try:
            export(self.symbol, self.data, (self.hist, self.pc))
        except AttributeError:
            self.err_msg('Nothing to export')

    def build_stats(self, data:dict = {}):
        # ticker statistics table
        f_y = 0.35
        f_hgt = 1 - f_y

        self.stats_frame = ctk.CTkFrame(self.data_frame)
        self.stats_frame.place(relx = 0, rely = f_y, relwidth = 1, relheight = f_hgt)

        index = ['Samples', 'Start Date', 'End Date', 'Mean ($)', 'Median ($)', 'Mode ($)', 'Std. Dev. ($)', 'Variance ($)', 'Skewness', 'Kurtosis']

        # columns 
        for i, idx in enumerate(index):
            y = (i * 25) + 5
            self.index_label = ctk.CTkLabel(self.stats_frame, text = idx)
            self.index_label.place(x = 20, y = y)

        if len(data) == len(index):
            self.update_statistics(data)

        # create export button
        self.export_button = ctk.CTkButton(self.stats_frame, text = 'Export', command = self.export_data, width = 220)
        self.export_button.place(x = 10, rely = 0.87)

        
    def update_statistics(self, data:dict = {}):
        for i, d in enumerate(data):
            y = (i * 25) + 5
            self.data_label = ctk.CTkLabel(self.stats_frame, text = data[d])
            self.data_label.place(x = 130, y = y)
  
  

    def build_main_header(self):
        # main header
        self.main_header = ctk.CTkLabel(self.header_frame,
                        text = title, font = ctk.CTkFont(size = 20, weight = 'bold')).pack(expand = True)
        

    def plot_fig(self, master, fig):

        # plot matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master = master)
        canvas.draw()
        
        self.cv = canvas.get_tk_widget()
        self.cv.pack(expand = True, anchor = 's', padx = 5, pady = 5)
        
    
    def fetch_data(self, symbol: str = '', samples: str = ''):
        self.err_msg()
        self.data = None
        # validate entry, if pass, proceed to fetching data 
        try:
            sym_entry = self.symbol_entry.get().strip().upper()
            smpl_entry = self.sample_entry.get().strip()

            self.symbol = symbol if sym_entry == '' else sym_entry 
            self.samples = samples if smpl_entry == '' else smpl_entry
            self.symbol, self.samples = validate_entry(self.symbol, self.samples)

        except ValueError:
            # symbol input is empty
            self.err_msg('Invalid Symbol Entry')
            return None
        except AssertionError:
            # samples input 
            self.err_msg('Invalid Samples Entry')
            return None


        try:
            self.data, self.close = build_data(self.symbol, int(self.samples))

            self.hist, self.pc = plot_data(self.close, self.data, self.symbol)
            self.update_statistics(self.data)
            self.tab_func()
        except ValueError:
            # print error message on ui
            self.err_msg(f'No data for symbol: {symbol}')
            return None 
        except AssertionError:
            self.err_msg(f'Invalid Samples')
            return None
        except AttributeError:
            self.err_msg('No data')
            return None
        
        return symbol, samples

    def err_msg(self, err_msg: str = ''):

        # error message 
        self.message.configure(text = err_msg, text_color = 'red')



def main():
    app = App()
    app.mainloop()

def validate_entry(symbol:str = '', samples:str = ''):
        '''
        testing: symbol and samples == '' raises value error
        letters in samples raises assertion error
        '''
        # get entry field values

        # compare: (func parameters are only used for unit testing)
        # use func parameters if input fields are empty

        # main validation: 
        # symbol = valid string
        # sample is numeric
        
        # check if fields are not empty
        # leave this portion below assignment, otherwise, testing will be faulty
        if symbol == '' or samples == '':
            raise ValueError
        
        # check if if input samples is numeric
        assert samples.isnumeric()

        return symbol, int(samples)




def download(symbol:str = 'AAPL', samples:int = 10):
    '''
    # testing: samples assertion 
    # output type: dataframe
    # output shape (samples, columns (6))
    # test wrong symbol raises value error
    '''
    print('downloading')
    
    df = yf.download(symbol, interval = '1d').tail(samples)
    if df.empty:
        raise ValueError(f'No data for symbol: {symbol}')
    
    return df

def build_data(symbol:str = 'AAPL', samples:int = 10):
    '''
    testing: samples assertion
    output type: list, pd.series
    lower case symbol
    '''
    assert samples > 5
    df = download(symbol.upper(), samples)
    close = df['Close']

    mean, median, mode = np.mean(close), np.median(close), sc.mode(close, keepdims = True)
    var, skew, kurt, sdev = np.var(close), sc.skew(close), sc.kurtosis(close), math.sqrt(np.var(close))
    start_date = df.index[0].strftime('%m/%d/%Y')
    end_date = df.index[-1].strftime('%m/%d/%Y')
    main_data = [samples, start_date, end_date, mean, median.item(), mode[0][0].item(), sdev, var, skew, kurt]
    updated = [round(d, 2) if type(d) == float else d for d in main_data]
    key = ['samples','start','end','mean','median','mode','sdev','var','skew','kurt']
    data = {k:v for k,v in zip(key,updated)}


    return data, close

def plot_data(data:pd.Series, main_data:dict, symbol:str):
    samples = main_data['samples']
    mean = main_data['mean']
    sdev = main_data['sdev']
    var = main_data['var']
    skew = main_data['skew']
    kurt = main_data['kurt']
    
    close_label = f'Close - {symbol} | {samples} days'
    fs = 8
    fc = '#EAEAF2'
    fig_w, fig_h = 5, 4.2

    # hist portion
    hist, axh = plt.subplots(facecolor = fc, edgecolor = 'black')
    hist.set_size_inches(fig_w, fig_h)
    axh.clear()
    axh = sns.distplot(data, kde = True, bins = 10)
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
    plt.plot(data, label = 'Close')
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

def export(sym: str, main_data: dict, figs:tuple = None):
    '''
    EXPORTING TO PDF: 
    1. convert figure to image
    2. add image to pdf
    '''
    smpl = main_data['samples']
    start_date = main_data['start']
    end_date = main_data['end']
    p = 'exports'
    if not os.path.exists(p):
        os.mkdir(p)

    today = dt.today().strftime('%Y%m%d')
    fig_path = f'exports/{sym}_{smpl}_{today}'
    if not os.path.exists(fig_path):
        os.mkdir(fig_path)

    hist_path = f'{fig_path}/{sym}_{smpl}_hist.jpg'
    pc_path = f'{fig_path}/{sym}_{smpl}_pc.jpg'
    pdf_path = f'{fig_path}/{sym}_{smpl}.pdf'
    
    hist, pc = figs[0], figs[1]
    hist.savefig(hist_path, dpi = 300)
    pc.savefig(pc_path, dpi = 300)

    title = f'{sym} {smpl}-day Summary'
    dates = f'{start_date} to {end_date}'
    #pdf 
    page_width, page_height = 210, 297
    pdf = FPDF(orientation = 'portrait', format = 'A4', unit = 'mm')
    pdf.set_margins(0, 0, 0)
    pdf.add_page()
    pdf.set_y(10)
    pdf.set_font('helvetica', size = 30)
    pdf.cell(w = page_width, h = 20, text = title, align = 'C')

    pdf.set_y(20)
    pdf.set_font('helvetica', size = 12)
    pdf.cell(w = page_width, h = 20, text = dates, align = 'C')

    pdf.image(hist_path, x = 35, y = 40, w = page_width * 0.65, keep_aspect_ratio=True)
    pdf.image(pc_path, x = 35, y = 165, w = page_width * 0.65,keep_aspect_ratio=True)

    pdf.output(pdf_path)



    
'''
PROJECT TODOS
- main function DONE
- 3 or more additional functions, and must be accompanied with pytest DONE
- mainfile: project.py DONE
- additional functions must be standalone (same level as main) DONE
- test: test_project.py DONE
- pip installable libraries in a file called "requirements.txt"

'''



if __name__ == "__main__":
    main()