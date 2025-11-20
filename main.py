from tkinter import *
from view import interfaces

if __name__ == "__main__":
    window = Tk()
    app = interfaces.Vista(window)
    window.mainloop()