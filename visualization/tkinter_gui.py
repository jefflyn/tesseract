#! /usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import tkinter as tk
import serial.tools.list_ports
from tkinter import ttk
from tkinter import scrolledtext

SerialPort = serial.Serial()
GUI = tk.Tk()  # 父容器
GUI.title("Serial Tool")  # 父容器标题
GUI.geometry("440x320")  # 父容器大小

Information = tk.LabelFrame(GUI, text="操作信息", padx=10, pady=10)  # 水平，垂直方向上的边距均为10
Information.place(x=20, y=20)
Information_Window = scrolledtext.ScrolledText(Information, width=20, height=5, padx=10, pady=10, wrap=tk.WORD)
Information_Window.grid()

Send = tk.LabelFrame(GUI, text="发送指令", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
Send.place(x=240, y=20)

DataSend = tk.StringVar()  # 定义DataSend为保存文本框内容的字符串

EntrySend = tk.StringVar()
Send_Window = ttk.Entry(Send, textvariable=EntrySend, width=23)
Send_Window.grid()


def WriteData():
    global DataSend
    DataSend = EntrySend.get()
    Information_Window.insert("end", '发送指令为：' + str(DataSend) + '\n')
    Information_Window.see("end")
    SerialPort.write(bytes(DataSend, encoding='utf8'))


tk.Button(Send, text="发送", command=WriteData).grid(pady=5, sticky=tk.E)

Receive = tk.LabelFrame(GUI, text="接收区", padx=10, pady=10)  # 水平，垂直方向上的边距均为 10
Receive.place(x=240, y=124)
Receive_Window = scrolledtext.ScrolledText(Receive, width=18, height=9, padx=8, pady=10, wrap=tk.WORD)
Receive_Window.grid()

option = tk.LabelFrame(GUI, text="选项", padx=10, pady=10)  # 水平，垂直方向上的边距均为10
option.place(x=20, y=150, width=203)  # 定位坐标
# ************创建下拉列表**************
ttk.Label(option, text="串口号:").grid(column=0, row=0)  # 添加串口号标签
ttk.Label(option, text="波特率:").grid(column=0, row=1)  # 添加波特率标签

Port = tk.StringVar()  # 端口号字符串
Port_list = ttk.Combobox(option, width=12, textvariable=Port, state='readonly')
ListPorts = list(serial.tools.list_ports.comports())
Port_list['values'] = [i[0] for i in ListPorts]
Port_list.current(0)
Port_list.grid(column=1, row=0)  # 设置其在界面中出现的位置  column代表列   row 代表行

BaudRate = tk.StringVar()  # 波特率字符串
BaudRate_list = ttk.Combobox(option, width=12, textvariable=BaudRate, state='readonly')
BaudRate_list['values'] = (1200, 2400, 4800, 9600, 14400, 19200, 38400, 43000, 57600, 76800, 115200)
BaudRate_list.current(3)
BaudRate_list.grid(column=1, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行

switch = tk.LabelFrame(GUI, text="", padx=10, pady=10)  # 水平，垂直方向上的边距均为 10
switch.place(x=20, y=250, width=203)  # 定位坐标


def ReceiveData():
    while SerialPort.isOpen():
        Receive_Window.insert("end", str(SerialPort.readline()) + '\n')
        Receive_Window.see("end")


def Close_Serial():
    SerialPort.close()


def Open_Serial():
    if not SerialPort.isOpen():
        SerialPort.port = Port_list.get()
        SerialPort.baudrate = BaudRate_list.get()
        SerialPort.timeout = 0.1
        SerialPort.open()
        if SerialPort.isOpen():
            t = threading.Thread(target=ReceiveData)
            t.setDaemon(True)
            t.start()
    else:
        SerialPort.close()


tk.Button(switch, text="开始采集", command=Open_Serial).pack(side="left", padx=13)
tk.Button(switch, text="停止采集", command=Close_Serial).pack(side="right", padx=13)

GUI.mainloop()
