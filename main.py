from finstats.app import App
from threading import Thread

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    t = Thread(target = main)
    t.start()