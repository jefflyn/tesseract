from tkinter import * 
import random

from stocks.app import realtime

def showrealtime(data=None):
    var.set(str(data))
    label.after(3000, showrealtime, data)

if __name__ == '__main__':
    root = Tk()
    var = StringVar()
    label = Label(root, textvariable=var)

    label.pack()
    showrealtime(data=realtime.get_realtime('cf'))

    root.mainloop()