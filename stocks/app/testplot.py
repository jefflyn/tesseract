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

# https://segmentfault.com/a/1190000006158803
# http://blog.csdn.net/jtscript/article/details/44928535
if __name__ == '__main__':
    plt.subplot(211)
    # 生成横纵坐标信息
    dates = ['2017-11-02', '2017-11-23', '2017-12-04', '2018-01-02', '2018-01-03', '2018-01-04']
    xs = [datetime.strptime(d, '%Y-%m-%d').date() for d in dates]

    ys = [15.2, 13, 14.8, 15, 13.5, 14.1]
    xs = range(0, len(ys))
    # 配置横坐标
    ax = plt.gca()
    # ax.set_xticks(np.linspace(0, 1, 9))
    ax.set_xticklabels(('2017-11-02', '2017-11-23', '2017-12-04', '2018-01-02', '2018-01-03', '2018-01-04'))

    # ax.get_xaxis().get_major_formatter().set_useOffset(False)
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.title('A Simple Plot')
    plt.legend(loc=0)
    plt.xlabel('index')
    plt.ylabel('value')
    plt.grid(True)
    # 在折线图上标记数据，-+0.1是为了错开一点显示数据
    datadotxy = tuple(zip(xs,ys))
    for dotxy in datadotxy:
        ax.annotate(str(dotxy[1]), xy=dotxy)

    # 将X轴格式化为日期形式
    # ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    # fig.autofmt_xdate()

    # Plot
    plt.plot(xs, ys, 'ro-', label='xxxxx')

    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.show()