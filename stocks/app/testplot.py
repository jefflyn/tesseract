from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.header import Header
from IPython.display import HTML
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from stocks.app import realtime
from stocks.app import falco
from stocks.app import _utils
from stocks.data import _datautils
from stocks.gene import limitup
from stocks.gene import period
from stocks.gene import maup
from stocks.gene import bargain

def test1():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plot_data = [1.7, 1.7, 1.7, 1.54, 1.52]
    xdata = range(len(plot_data))
    labels = ["2009-June", "2009-Dec", "2010-June", "2010-Dec", "2011-June"]
    ax.plot(xdata, plot_data, "b-")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticks([1.4, 1.6, 1.8])

    # grow the y axis down by 0.05
    ax.set_ylim(1.35, 1.8)
    # expand the x axis by 0.5 at two ends
    ax.set_xlim(-0.5, len(labels) - 0.5)

    plt.show()

# https://segmentfault.com/a/1190000006158803
# http://blog.csdn.net/jtscript/article/details/44928535
# http://blog.csdn.net/wl_ss/article/details/78449441
if __name__ == '__main__':
    # test1()

    plt.subplot(211)
    # 生成横纵坐标信息
    labels = ['2017-11-02', '2017-11-23', '2017-12-04', '2018-01-02', '2018-01-03', '2018-01-04']
    xs = [datetime.strptime(d, '%Y-%m-%d').date() for d in labels]
    xs = np.arange(len(labels))
    ys = [15.2, 13, 14.8, 15, 13.5, 14.1]

    newx = []
    newy = []
    for n in range(len(ys)):
        if n < len(ys) - 1:
            startx = xs[n]
            starty = ys[n]
            nextx = xs[n + 1]
            nexty = ys[n + 1]
            midx = (startx + nextx) / 2
            midy = (starty + nexty) / 2
            newx.append(midx)
            newy.append(midy)

    # 配置横坐标
    ax = plt.gca()
    ax.set_xticks(xs)
    ax.set_xticklabels(labels)
    ax.set_xlim(-0.5, len(labels) - 0.5)
    # ax.set_ylim(-1, len(ys) - 1)
    # ax.get_xaxis().get_major_formatter().set_useOffset(False)
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.title('A Simple Plot')
    plt.legend(loc=0)
    # plt.xlabel('index')
    plt.ylabel('value')
    plt.grid(True)
    # 在折线图上标记数据
    datadotxy = tuple(zip(xs, ys))
    spacexy = tuple(zip(newx, newy))
    for dotxy in datadotxy:
        ax.annotate(str(dotxy[1]), xy=dotxy)

    for spxy in spacexy:
        ax.annotate(str('9%'), xy=spxy)

    # 将X轴格式化为日期形式
    # ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    # fig.autofmt_xdate()

    # Plot
    plt.plot(xs, ys, 'ro-', label='xxxxx')

    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.show()