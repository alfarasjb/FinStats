'''
TODOS

triggered by thread: target by ops
set app value 
'''

#from project import App
from .calc import Calc

class Event_Handler:
    def __init__(self):
        pass

    def download_event(self, app, symbol, samples):
        self.c = Calc(symbol, samples)
        # triggers build data
        # once this is called, set app is 
        
        # once function has returned, set app is not loading
      
        app.data, app.close = self.c.build_data()
       

        app.is_loading = False

        # used for testing only
        return app.data, app.close
    
    def plot_event(self):
        hist, pc = self.c.plot_data()
        return hist, pc