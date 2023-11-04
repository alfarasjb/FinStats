import warnings
from threading import Thread
import customtkinter as ctk
from PIL import ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .ops import Ops


warnings.filterwarnings('ignore')

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('green')

title = 'FinStats'
w, h = 800, 550
icon = 'finstats/icon.png'


class App(ctk.CTk):


    def __init__(self):
        super().__init__()

        self.cv, self.symbol, self.samples, self.data = None, None, None, None
        
        # WINDOW CONFIG
        self.title(title)
        self.wm_iconbitmap()
        self.iconphoto(True, ImageTk.PhotoImage(file = icon))
        self.geometry(f'{w}x{h}')
        self.maxsize(w, h)
        self.minsize(w, h)

        # Building UI
        self.build_parent_frames()
        self.build_main_header()
        self.build_input_fields()
        self.build_stats()
        self.build_tabview()

        self.message = None
        self.is_loading = False

    ### ========== UI METHODS ========== ###
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
    

    def build_main_header(self):
        # main header
        self.main_header = ctk.CTkLabel(self.header_frame,
                        text = title, font = ctk.CTkFont(size = 20, weight = 'bold')).pack(expand = True)


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

        self.symbol_name.grid(row = 0, column = 0, padx = (20, 5), pady = (15, 5))
        self.sample_size.grid(row = 1, column = 0, padx = (20, 5), pady = 5)
        self.symbol_entry.grid(row = 0, column = 1, padx = (5, 10), pady = (15, 5))
        self.sample_entry.grid(row = 1, column = 1, padx = (5, 10), pady = 5)
        self.fetch_button.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 5)


    def build_stats(self, data:dict = {}):
        # ticker statistics table
        f_y = 0.35
        f_hgt = 1 - f_y
        self.stats_frame = ctk.CTkFrame(self.data_frame)
        self.stats_frame.place(relx = 0, rely = f_y, relwidth = 1, relheight = f_hgt)

        # columns 
        index = ['Samples', 'Start Date', 'End Date', 'Mean ($)', 'Median ($)', 'Mode ($)', 'Std. Dev. ($)', 'Variance ($)', 'Skewness', 'Kurtosis']
        for i, idx in enumerate(index):
            y = (i * 25) + 5
            self.index_label = ctk.CTkLabel(self.stats_frame, text = idx)
            self.index_label.place(x = 20, y = y)

        if len(data) == len(index):
            self.update_statistics(data)

        # create export button
        self.export_button = ctk.CTkButton(self.stats_frame, text = 'Export', command = self.export_data, width = 220)
        self.export_button.place(x = 10, rely = 0.87)


    def build_tabview(self):
        # tabview
        tab_names = ['Histogram', 'Price']

        self.tabview = ctk.CTkTabview(self.plot_frame, command = self.tab_func)
        self.tabview.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        [self.tabview.add(tab_name) for tab_name in tab_names]

    ### ========== UI METHODS ========== ###

    ### ========== UI COMMANDS ========== ###
    def tab_func(self):
        # parent: tabview
        name = self.tabview.get()
        master = self.tabview.tab(name)
        
        if self.cv is not None:
            self.cv.pack_forget()
        
        if name == 'Histogram':
            self.plot_fig(master, self.hist)
    
        elif name == 'Price':
            self.plot_fig(master, self.pc)
    

    def export_data(self):
        # parent: export
        try:
            fig_path = self.ops.export(self.data, (self.hist, self.pc))
            self.msg(f'Exported to: {fig_path}', 'confirm')
        except AttributeError:
            self.msg('Nothing to export')


    def fetch_data(self, symbol: str = '', samples: str = ''):
        # parent: fetch
        self.msg()
        self.data = None

        # create ops here
        

        # validate entry, if pass, proceed to fetching data 
        try:
            sym_entry = self.symbol_entry.get().strip().upper()
            smpl_entry = self.sample_entry.get().strip()

            self.symbol = symbol if sym_entry == '' else sym_entry 
            self.samples = samples if smpl_entry == '' else smpl_entry
            #self.symbol, self.samples = validate_entry(self.symbol, self.samples)
            self.ops = Ops(self.symbol, self.samples)
            self.symbol, self.samples = self.ops.validate_entry()

        except ValueError:
            # symbol input is empty
            self.msg('Invalid Symbol Entry')
            return None
        except AssertionError:
            # samples input 
            self.msg('Invalid Samples Entry')
            return None

        try:
            #self.data, self.close = build_data(self.symbol, int(self.samples))
            # CREATE PROGRESS BAR HERE
            self.msg(type = 'load')
            #start_download_thread(self, self.symbol, self.samples)
            self.ops.start_download_thread(self)
            self.after(1000, self.check_if_done)

            
        except ValueError:
            # print error message on ui
            self.msg(f'No data for symbol: {symbol}')
            return None 
        except AssertionError:
            self.msg(f'Invalid Samples')
            return None
        except AttributeError:
            self.msg('No data')
            return None
        
        return symbol, samples
    ### ========== UI COMMANDS ========== ###


    ### ========== UI UPDATES / UTILITIES ========== ###
    def update_statistics(self, data:dict = {}):
        for i, d in enumerate(data):
            y = (i * 25) + 5
            self.data_label = ctk.CTkLabel(self.stats_frame, text = data[d])
            self.data_label.place(x = 130, y = y)
  

    def plot_fig(self, master, fig):

        # plot matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master = master)
        canvas.draw()
        
        self.cv = canvas.get_tk_widget()
        self.cv.pack(expand = True, anchor = 's', padx = 5, pady = 5)
          

    def check_if_done(self):
        if not self.is_loading:
            # END PROGRESS BAR HERE
            self.message.destroy()
            try:
                #self.hist, self.pc = plot_data(self.close, self.data, self.symbol)
                self.hist, self.pc = self.ops.plot()
                self.update_statistics(self.data)
                self.tab_func()
            except AttributeError:
                self.msg(f'No data for symbol: {self.symbol}')
                return None
        else:
            self.after(1000,self.check_if_done)


    def msg(self, err_msg: str = '', type:str = 'err'):
        master = self.input_field_frame
        if self.message is not None:
            self.message.destroy()
        
        if type == 'load':
            self.message = ctk.CTkProgressBar(master, orientation = 'horizontal', mode = 'indeterminate')
            self.message.grid(row = 3, column = 0, columnspan = 2, padx = 10, pady = (10,0))   
            self.message.start()

        else:
            # error message
            col = 'red' if type == 'err' else 'green'
            self.message = ctk.CTkLabel(master, text = err_msg, text_color=col)
            self.message.grid(row = 3, column = 0, columnspan = 2, padx = 10, pady = 0)
            
            # loading progress bar
            

    ### ========== UI UPDATES / UTILITIES ========== ###

