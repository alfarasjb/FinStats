'''
TODO

methods: 
Validation 
Exports
'''
import os
from datetime import datetime as dt
from fpdf import FPDF
from threading import Thread 
from .event import Event_Handler

class Ops:
    
    def __init__(self, symbol:str, samples:str):
        self.symbol = symbol 
        self.samples = samples 
    
        self.ev = Event_Handler()

    def validate_entry(self):
        print(self.symbol, self.samples)
        if self.symbol == '' or self.samples == '':
            raise ValueError

        assert self.samples.isnumeric()
        self.samples = int(self.samples)
        return self.symbol, self.samples

    def start_download_thread(self, app) -> bool:
        app.is_loading = True
        b = Thread(target = self.ev.download_event, args = [app, self.symbol, self.samples])
        b.start()

    def plot(self):
        hist, pc = self.ev.plot_event()
        return hist, pc


    def export(self, main_data:dict, figs:tuple):
        start_date = main_data['start']
        end_date = main_data['end']

        # check if exports folder exists
        p = 'exports'
        if not os.path.exists(p):
            os.mkdir(p)

        # check data directory exists
        today = dt.today().strftime('%Y%m%d')
        folder = f'{self.symbol}_{self.samples}_{today}'
        fig_path = f'{p}/{folder}'
        if not os.path.exists(fig_path):
            os.mkdir(fig_path)

        # export filenames
        hist_path = f'{fig_path}/{self.symbol}_{self.samples}_hist.jpg'
        pc_path = f'{fig_path}/{self.symbol}_{self.samples}_pc.jpg'
        pdf_path = f'{fig_path}/{self.symbol}_{self.samples}.pdf'

        # export figures as image, and import into pdf
        hist, pc = figs[0], figs[1]
        hist.savefig(hist_path, dpi = 300)
        pc.savefig(pc_path, dpi = 300)

        title = f'{self.symbol} {self.samples}-day Summary'
        dates = f'{start_date} to {end_date}'

        # pdf 
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

        return folder
