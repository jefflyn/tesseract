from datetime import datetime

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('TkAgg')
matplotlib.rcParams['font.sans-serif'] = 'SimHei'
import matplotlib.pyplot as plt
from zillion.stock.data import data_util



def get_bottom(df=None, limit=20):
    """
    take the bottom price when droped more than 20% by default
    """
    starttime = datetime.now()
    if df is None:
        return df
    groupdf = df.groupby("code")
    dfresult = []
    for code, group in groupdf:
        # print(code)
        # print(group)
        size = group.iloc[:, 0].size
        startfromlast = 1
        lastestrec = group.tail(startfromlast)
        idx = lastestrec.index.to_numpy()[0]
        status = lastestrec.at[idx, 'status']
        bottom = lastestrec.at[idx, 'begin_price'] if status == 'up' else lastestrec.at[idx, 'end_price']
        bottom_price = bottom
        top = lastestrec.at[idx, 'end_price'] if status == 'up' else lastestrec.at[idx, 'begin_price']

        reclist = []
        while startfromlast < size:
            startfromlast += 1
            lastrec = group.tail(startfromlast)
            idx_list = lastrec.index.to_numpy()
            lastidx = idx_list[0]
            laststatus = lastrec.at[lastidx, 'status']
            lastp = lastrec.at[lastidx, 'change']
            # val = lastp[0:len(lastp)-1]
            if abs(float(lastp)) < limit:
                continue
            else:
                bottom_price = lastrec.at[lastidx, 'begin_price'] if laststatus == 'up' else lastrec.at[
                    lastidx, 'end_price']
                if size == 1:
                    top = lastrec.at[lastidx, 'end_price'] if laststatus == 'up' else lastrec.at[lastidx, 'begin_price']
                else:
                    if lastidx == size - 1:  # last one
                        if laststatus == 'up':
                            # get previous down one
                            top = lastrec.at[lastidx - 1, 'begin_price']
                        else:
                            top = lastrec.at[lastidx, 'begin_price']
                    else:
                        top = lastrec.at[lastidx, 'end_price'] if laststatus == 'up' else lastrec.at[
                            lastidx, 'begin_price']

                break
        reclist.append(code)
        reclist.append(bottom if bottom < bottom_price else bottom_price)
        reclist.append(top)
        # add three buy positions for wave periods
        reclist.append(top * 0.66)
        reclist.append(top * 0.5)
        reclist.append(top * 0.33)
        dfresult.append(reclist)

    result = pd.DataFrame(dfresult, columns=['code', 'bottom', 'top', 'buy1', 'buy2', 'buy3'])

    endtime = datetime.now()
    # print("total time: %ds" % (endtime - starttime).seconds)
    return result


def plot_wave(dflist=None, filename='wave.png', title='', columns=1):
    size = len(dflist)
    cols = columns
    rows = size / cols if (size % cols == 0) else int(size / cols + 1)
    cols = size if size < cols else cols
    plt.figure(figsize=(cols * 8, rows * 5))
    # plt.gcf().suptitle(title + '波段图', color='orangered', fontsize=20, fontweight='bold')
    for idx in range(size):
        df = dflist[idx]
        # subplot()
        plt.subplot(rows, cols, idx + 1)
        # 生成横纵坐标信息
        # labels = ['2017-01-03', '2017-02-23', '2017-05-24', '2017-08-04', '2017-12-06', '2018-01-05']

        labels = list(df['date'])
        xs = np.arange(len(labels))
        # ys = [28.51, 32.50, 13.68, 22.56, 14.0, 16.9]
        ys = list(df['price'])

        code = list(df['code'])[0]
        name = list(df['name'])[0]

        daymap = {}
        dayx = list(map(lambda x: x + 0.5, xs))[0: len(ys)]
        dayy = [min(ys) * 0.6] * (len(ys) - 1)
        changemap = {}
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
                changemap[midx] = round((nexty - starty) / starty * 100, 2)
                begindate = labels[n]
                enddate = labels[n + 1]
                daymap[dayx[n]] = (
                        datetime.strptime(enddate, '%Y-%m-%d') - datetime.strptime(begindate, '%Y-%m-%d')).days

        # 配置横坐标
        ax = plt.gca()

        ax.set_xticks(xs)
        # labels = list(map(lambda x: x.replace('-', ''), labels))
        labels = list(map(lambda x: x[2:], labels))
        ax.set_xticklabels(labels, rotation=25, fontsize=10)

        ax.set_xlim(-0.5, len(labels) - 0.5)
        ax.set_ylim(min(ys) * 0.5, max(ys) * 1.2)

        plt.title(name, fontweight='bold')
        plt.legend(loc=0)
        # plt.xlabel('index')
        plt.ylabel('price')
        plt.grid(True)
        ax.yaxis.grid(True, which='major')
        # 在折线图上标记数据
        datadotxy = tuple(zip(xs, ys))
        flag = 0 if ys[0] < ys[1] else 1  # 判断第一个值是否底部
        for dotx, doty in datadotxy:
            if dotx % 2 == flag:  # 低点，调整底部往下一点
                dotxy = (dotx - 0.2, round(doty * 0.9, 2))
                ax.annotate(str(doty), xy=dotxy, fontsize=10, color='blue')
            else:
                dotxy = (dotx, round(doty + 1, 2))
                ax.annotate(str(doty), xy=dotxy, fontsize=10, color='red')

        spacexy = tuple(zip(newx, newy))
        for spxy in spacexy:
            dcolor = 'blue' if changemap[spxy[0]] < 0 else 'red'
            ax.annotate(str(changemap[spxy[0]]) + '%', ha='center', xy=spxy, fontsize=10, color=dcolor)
        # arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3', facecolor='yellow'), xytext=(3, 1.5)
        dayxy = tuple(zip(dayx, dayy))
        for dxy in dayxy:
            ax.annotate(str(daymap[dxy[0]]) + 'd', ha='center', xy=dxy, fontsize=10, color='green')

        # Plot
        plt.plot(xs, ys, 'ko')
        line = plt.plot(xs, ys, 'r:', label='price')
        # plt.gcf().autofmt_xdate()  # 自动旋转日期标记
        ax.legend(line, (code,))

    plt.savefig(filename, dpi=100, bbox_inches='tight')
    # plt.show()


def format_wave_data(wavedf=None, is_index=False):
    latestone = wavedf.tail(1)  # get the newest record
    if latestone.empty is True:
        return None
    i = latestone.index.to_numpy()[0]
    code = latestone.at[i, 'code']
    stock = data_util.get_basics(code, index=is_index)
    name = stock if isinstance(stock, str) else stock.at[stock.index.to_numpy()[0], 'name']
    enddate = latestone.at[latestone.index.to_numpy()[0], 'end']
    endprice = latestone.at[latestone.index.to_numpy()[0], 'end_price']

    codes = list(wavedf['code'])
    codes.append(code)
    names = [name] * len(codes)
    dates = list(wavedf['begin'])
    dates.append(enddate)
    prices = list(wavedf['begin_price'])
    prices.append(endprice)
    newwavedf = pd.DataFrame({'code': codes, 'name': names, 'date': dates, 'price': prices})
    return newwavedf

