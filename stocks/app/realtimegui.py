from tkinter import *


def onGo():
    def counter(i):
        if i > 0:
            t.delete()
            t.insert(END, 'a_' + str(i))
            t.after(1000, counter, i - 1)
        else:
            goBtn.config(state=NORMAL)

    goBtn.config(state=DISABLED)
    counter(50)


root = Tk()
t = Text(root)
t.pack()
goBtn = Button(text="Go!", command=onGo)
goBtn.pack()
root.mainloop()