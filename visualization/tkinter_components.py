#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext  # 导入滚动文本框的模块

win = tk.Tk()
win.title("Python GUI")  # 添加标题

ttk.Label(win, text="Chooes a number").grid(column=1, row=0)  # 添加一个标签，并将其列设置为1，行设置为0
ttk.Label(win, text="Enter a name:").grid(column=0, row=0)  # 设置其在界面中出现的位置  column代表列   row 代表行


# button被点击之后会被执行
def clickMe():  # 当acction被点击时,该函数则生效
    action.configure(text='Hello ' + name.get() + ' ' + numberChosen.get())  # 设置button显示的内容
    print('check3 is %s %s' % (type(chvarEn.get()), chvarEn.get()))


# 按钮
action = ttk.Button(win, text="Click Me!", command=clickMe)  # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
action.grid(column=2, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行

# 文本框
name = tk.StringVar()  # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
nameEntered = ttk.Entry(win, width=12, textvariable=name)  # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
nameEntered.grid(column=0, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
nameEntered.focus()  # 当程序运行时,光标默认会出现在该文本框中

# 创建一个下拉列表
number = tk.StringVar()
numberChosen = ttk.Combobox(win, width=12, textvariable=number, state='readonly')
numberChosen['values'] = (1, 2, 4, 42, 100)  # 设置下拉列表的值
numberChosen.grid(column=1, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

# 复选框
chVarDis = tk.IntVar()  # 用来获取复选框是否被勾选，通过chVarDis.get()来获取其的状态,其状态值为int类型 勾选为1  未勾选为0
check1 = tk.Checkbutton(win, text="Disabled", variable=chVarDis,
                        state='disabled')  # text为该复选框后面显示的名称, variable将该复选框的状态赋值给一个变量，当state='disabled'时，该复选框为灰色，不能点的状态
check1.select()  # 该复选框是否勾选,select为勾选, deselect为不勾选
check1.grid(column=0, row=4,
            sticky=tk.W)  # sticky=tk.W  当该列中其他行或该行中的其他列的某一个功能拉长这列的宽度或高度时，设定该值可以保证本行保持左对齐，N：北/上对齐  S：南/下对齐  W：西/左对齐  E：东/右对齐

chvarUn = tk.IntVar()
check2 = tk.Checkbutton(win, text="UnChecked", variable=chvarUn)
check2.deselect()
check2.grid(column=1, row=4, sticky=tk.W)

chvarEn = tk.IntVar()
check3 = tk.Checkbutton(win, text="Enabled", variable=chvarEn)
check3.select()
check3.grid(column=2, row=4, sticky=tk.W)

# 单选按钮

# 定义几个颜色的全局变量
COLOR1 = "Blue"
COLOR2 = "Gold"
COLOR3 = "chocolate1"


# 单选按钮回调函数,就是当单选按钮被点击会执行该函数
def radCall():
    radSel = radVar.get()
    if radSel == 1:
        win.configure(background=COLOR1)  # 设置整个界面的背景颜色
    elif radSel == 2:
        win.configure(background=COLOR2)
    elif radSel == 3:
        win.configure(background=COLOR3)

radVar = tk.IntVar()  # 通过tk.IntVar() 获取单选按钮value参数对应的值
rad1 = tk.Radiobutton(win, text=COLOR1, variable=radVar, value=1, command=radCall)  # 当该单选按钮被点击时，会触发参数command对应的函数
rad1.grid(column=0, row=5, sticky=tk.W)  # 参数sticky对应的值参考复选框的解释

rad2 = tk.Radiobutton(win, text=COLOR2, variable=radVar, value=2, command=radCall)
rad2.grid(column=1, row=5, sticky=tk.W)

rad3 = tk.Radiobutton(win, text=COLOR3, variable=radVar, value=3, command=radCall)
rad3.grid(column=2, row=5, sticky=tk.W)

# 滚动文本框
scrolW = 30  # 设置文本框的长度
scrolH = 3  # 设置文本框的高度
scr = scrolledtext.ScrolledText(win, width=scrolW, height=scrolH, wrap=tk.WORD)
# wrap=tk.WORD   这个值表示在行的末尾如果有一个单词跨行，会将该单词放到下一行显示,比如输入hello，he在第一行的行尾,llo在第二行的行首,
# 这时如果wrap=tk.WORD，则表示会将 hello 这个单词挪到下一行行首显示, wrap默认的值为tk.CHAR
scr.grid(column=3, columnspan=3)  # columnspan 个人理解是将3列合并成一列   也可以通过 sticky=tk.W  来控制该文本框的对齐方式
win.mainloop()  # 当调用mainloop()时,窗口才会显示出来
