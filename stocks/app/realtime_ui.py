import tkinter
import time
from tkinter import *
import stocks.app.realtime as realtime
from stocks.data import data_util as _dt

from tkinter import *
import time


def go():
      for i in range(500):
            text.delete('1.0', 'end')
            hold_df = _dt.get_my_stock_pool('df', 1)
            result = realtime.get_realtime(hold_df)
            text.insert(END, str(result))
            time.sleep(3)
            text.update()


root = Tk()
root.title('realtime live')
text = Text(root)
text.pack()

# 创建滚动条
scroll = tkinter.Scrollbar()
# 将滚动条填充
scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)  # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
text.pack(side=tkinter.LEFT, fill=tkinter.Y)  # 将文本框填充进窗口的左侧，
# 将滚动条与文本框关联
scroll.config(command=text.yview)  # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
text.config(yscrollcommand=scroll.set)  # 将滚动条关联到文本框

goBtn = Button(text="东方", command=go)
goBtn.pack(side=TOP)

root.mainloop()
