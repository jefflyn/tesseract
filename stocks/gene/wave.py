from datetime import date
from datetime import datetime
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
matplotlib.rcParams['font.sans-serif'] = 'SimHei'
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

import tushare as ts

from stocks.data import _datautils

pd.set_option('display.width', 600)

todaystr = datetime.now().strftime('%Y-%m-%d')

"""
take the bottom price when droped more than 20% by default
"""
def get_bottom(df = None, limit = 20):
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
        idx = lastestrec.index.get_values()[0]
        status = lastestrec.at[idx, 'status']
        bottom = lastestrec.at[idx, 'begin_price'] if status == 'up' else lastestrec.at[idx, 'end_price']
        top = lastestrec.at[idx, 'end_price'] if status == 'up' else lastestrec.at[idx, 'begin_price']

        reclist = []
        while startfromlast < size:
            startfromlast += 1
            lastrec = group.tail(startfromlast)
            lastidx = lastrec.index.get_values()[0]
            laststatus = lastrec.at[lastidx, 'status']
            lastp = lastrec.at[lastidx, 'change']
            # val = lastp[0:len(lastp)-1]
            if abs(float(lastp)) < limit:
                continue
            else:
                bottom = lastrec.at[lastidx, 'begin_price'] if laststatus == 'up' else lastrec.at[lastidx, 'end_price']
                if size == 1:
                    top = lastrec.at[lastidx, 'end_price'] if laststatus == 'up' else lastrec.at[lastidx, 'begin_price']
                else:
                    if lastidx == size - 1: #last one
                        if laststatus == 'up':
                            #get previous down one
                            top = lastrec.at[lastidx - 1, 'begin_price']
                        else:
                            top = lastrec.at[lastidx, 'begin_price']
                    else:
                        top = lastrec.at[lastidx, 'end_price'] if laststatus == 'up' else lastrec.at[lastidx, 'begin_price']



                break
        reclist.append(code)
        reclist.append(bottom)
        reclist.append(top)
        # add three buy positions for wave periods
        reclist.append(top*0.66)
        reclist.append(top*0.5)
        reclist.append(top*0.33)
        dfresult.append(reclist)

    result = pd.DataFrame(dfresult, columns=['code', 'bottom', 'top', 'buy1', 'buy2', 'buy3'])

    endtime = datetime.now()
    # print("total time: %ds" % (endtime - starttime).seconds)
    return result

"""
df: code name date price
"""
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
        dayx = list(map(lambda x : x + 0.5, xs))[0 : len(ys) ]
        dayy = [min(ys) * 0.6] * (len(ys) - 1)
        changemap = {}
        newx = []
        newy = []
        for n in range(len(ys)):
            if n < len(ys) - 1:
                startx = xs[n]
                starty = ys[n]
                nextx = xs[n+1]
                nexty = ys[n+1]
                midx = (startx + nextx) / 2
                midy = (starty + nexty) / 2
                newx.append(midx)
                newy.append(midy)
                changemap[midx] = round((nexty - starty) / starty * 100, 2)
                begindate = labels[n]
                enddate = labels[n+1]
                daymap[dayx[n]] = (datetime.strptime(enddate, '%Y-%m-%d') - datetime.strptime(begindate, '%Y-%m-%d')).days

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
        flag = 0 if ys[0] < ys[1] else 1 #判断第一个值是否底部
        for dotx, doty in datadotxy:
            if dotx%2 == flag: #低点，调整底部往下一点
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
        line = plt.plot(xs, ys, 'r:', label="price")
        # plt.gcf().autofmt_xdate()  # 自动旋转日期标记
        ax.legend(line, (code,))

    plt.savefig(filename, dpi=100, bbox_inches='tight')
    # plt.show()


def format_wave_data(wavedf=None, index=False):
    latestone = wavedf.tail(1) # get the newest record
    if latestone.empty == True:
        return None
    i = latestone.index.get_values()[0]
    code = latestone.at[i, 'code']
    stock = _datautils.get_basics(code, index=index)
    name = stock if isinstance(stock, str) else stock.at[stock.index.get_values()[0], 'name']
    enddate = latestone.at[latestone.index.get_values()[0], 'end']
    endprice = latestone.at[latestone.index.get_values()[0], 'end_price']

    codes = list(wavedf['code'])
    codes.append(code)
    names = [name] * len(codes)
    dates = list(wavedf['begin'])
    dates.append(enddate)
    prices = list(wavedf['begin_price'])
    prices.append(endprice)
    newwavedf = pd.DataFrame({'code': codes, 'name': names, 'date': dates, 'price': prices})
    return newwavedf


"""
default get the recent one year data
"""
def get_wave(codes=None, index=False, start=None, end=None, beginlow=True, duration=0, pchange=0):
    starttime = datetime.now()
    if start == None:
        bwdays = dt.timedelta(-730)
        start = (starttime + bwdays).strftime("%Y-%m-%d")
    # print("get wave start at [%s]" % starttime)
    code_list = []
    if isinstance(codes, str):
        code_list.append(codes)
    else: code_list = codes

    index_realtime = []
    if index == True:
        index_realtime = ts.get_index()
    perioddf_list = []
    for code in code_list:
        # print("   >>> processing %s ..." % code)
        # hist_data = ts.get_h_data(code, start)  # network issue
        hist_data = ts.get_k_data(code=code, index=index, start=start) #one day delay issue, use realtime interface solved
        if hist_data is None or len(hist_data) == 0:
            continue
        latestdate = hist_data.tail(1).at[hist_data.tail(1).index.get_values()[0], 'date']
        if todaystr != latestdate: # not the latest record
            if index == False:
                # get today data from [get_realtime_quotes(code)]
                realtime = ts.get_realtime_quotes(code)
                if realtime is None or realtime.empty == True:
                    continue
                todaylow = float(realtime.at[0, 'low'])
                if todaylow > 0:
                    newone = {'date':todaystr,'open':float(realtime.at[0,'open']),'close':float(realtime.at[0,'price']),'high':float(realtime.at[0,'high']), 'low':todaylow,'volume':int(float(realtime.at[0,'volume'])/100),'code':code}
                    newdf = pd.DataFrame(newone, index=[0])
                    hist_data = hist_data.append(newdf, ignore_index=True)
            else:
                indexdf = index_realtime[index_realtime['code'] == code]
                if indexdf is None or indexdf.empty == True:
                    continue
                index = indexdf.index.values[0]
                todaylow = float(indexdf.at[index, 'low'])
                if todaylow > 0:
                    newone = {'date': todaystr, 'open': float(indexdf.at[index, 'open']),
                              'close': float(indexdf.at[index, 'close']), 'high': float(indexdf.at[index, 'high']),
                              'low': todaylow, 'volume': int(float(indexdf.at[index, 'volume'])), 'code': code}
                    newdf = pd.DataFrame(newone, index=[0])
                    hist_data = hist_data.append(newdf, ignore_index=True)

        left_data = wavefrom(code, hist_data, beginlow, 'left', duration, pchange)
        #sorted by date asc
        left_data.reverse()
        right_data = wavefrom(code, hist_data, beginlow, 'right', duration, pchange)
        period_df = pd.DataFrame(left_data + right_data,columns=['code', 'begin', 'end', 'status', 'begin_price', 'end_price', 'days', 'change'])
        perioddf_list.append(period_df)
        # print("   >>> done!")

    if perioddf_list is None or len(perioddf_list) == 0:
        return 'result is empty, please check the code is exist!'
    result = pd.concat(perioddf_list, ignore_index=True)
    # result = result.sort_values(by=['code','begin'], axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')

    endtime = datetime.now()
    # print("get wave finish at [%s], total time: %ds" % (endtime, (endtime - starttime).seconds))
    return result


def wavefrom(code, df, beginlow, direction='left', duration=0, pchange=0):
    period_data = []
    # for get_k_data use
    firstdate = df.head(1).at[df.head(1).index.get_values()[0], 'date']
    lastdate = df.tail(1).at[df.tail(1).index.get_values()[0], 'date']
    # firstdate = datetime.utcfromtimestamp((df.tail(1).index.get_values()[0]).astype('O') / 1e9).strftime("%Y-%m-%d")
    # lastdate = datetime.utcfromtimestamp((df.head(1).index.get_values()[0]).astype('O') / 1e9).strftime("%Y-%m-%d")

    # start from the lowest price, find the wave from both sides
    pivot_low = df.min()['close'] if df.min()['low'] == 0 else df.min()['low']
    pivot_rec = df[df.low == pivot_low]
    # print(pivot_rec)
    pivot_index = pivot_rec.index.get_values()[0]
    pivot_date = pivot_rec.at[pivot_index, 'date']
    # pivot_date = datetime.utcfromtimestamp((pivot_rec.tail(1).index.get_values()[0]).astype('O') / 1e9).strftime("%Y-%m-%d")
    pivot_close = pivot_rec.at[pivot_index, 'close']

    ismax = beginlow
    begindate = firstdate
    enddate = pivot_date
    beginprice = pivot_low
    endprice = pivot_low

    if direction == 'right':
        begindate = pivot_date
        enddate = lastdate
    diff_days = datetime.strptime(enddate, '%Y-%m-%d') - datetime.strptime(begindate, '%Y-%m-%d')

    while diff_days.days > duration:
        data = df[(df.date >= begindate) & (df.date < enddate)] if direction == 'left' else df[(df.date > begindate) & (df.date <= enddate)]
        price = data.max()['high'] if ismax else data.min()['low']

        status = ''
        rec = data[data.high == price] if ismax else data[data.low == price]
        idx = rec.index.get_values()[0]
        date = rec.at[idx, 'date']
        close = rec.at[idx, 'close']

        if direction == 'left':
            beginprice = price
            begindate = date
            status = 'down' if ismax else 'up'
        if direction == 'right':
            #if the latest one, get the close price, calculate the actual rises
            endprice = close if date == lastdate else price
            enddate = date
            status = 'up' if ismax else 'down'

        diff_precent = (endprice - beginprice) / beginprice * 100
        if abs(diff_precent) < pchange:
            break
        list = []
        # ['code', 'begin', 'end', 'status' 'begin_price', 'end_price', 'days', 'p_change']
        list.append(code)
        list.append(begindate)
        list.append(enddate)
        list.append(status)
        list.append(beginprice)
        list.append(endprice)
        list.append((datetime.strptime(enddate, '%Y-%m-%d') - datetime.strptime(begindate, '%Y-%m-%d')).days)
        list.append(round(diff_precent, 2))
        if beginprice != endprice:
            period_data.append(list)

        if direction == 'left':
            begindate = firstdate
            enddate = date
            endprice = price
        if direction == 'right':
            begindate = date
            enddate = lastdate
            beginprice = price

        diff_days = datetime.strptime(enddate, '%Y-%m-%d') - datetime.strptime(begindate, '%Y-%m-%d')
        ismax = not ismax
    return period_data


def etl():
    from stocks.gene import limitup
    from stocks.gene import wave

    filePath = "../data/app/pa.txt"
    mystk = pd.read_csv(filePath, sep=' ')
    mystk['code'] = mystk['code'].astype('str').str.zfill(6)
    codes = list(mystk['code'])
    mywavedata = wave.get_wave(codes, start='2016-01-04')
    mywavedata.to_csv("../data/wavemy.csv", encoding='utf-8')


def wave_to_str(wavedf=None, size=4, change=10):
    if wavedf is None or size < 1:
        return ''
    changelist = list(wavedf['change'])
    # changelist = changelist[::-1]
    str_list = []
    sum_last = 0
    for i in range(0, len(changelist)):
        lastone = changelist[i]
        if abs(lastone) >= change:
            if sum_last != 0:
                str_list.append(sum_last)
                sum_last = 0
            str_list.append(lastone)
            continue
        else:
            sum_last += lastone
            if abs(sum_last) >= change:
                str_list.append(sum_last)
                sum_last = 0
                continue
            else:
                if i == len(changelist) - 1:
                    str_list.append(sum_last)
                    sum_last = 0
    takes = len(str_list) - size if len(str_list) - size > 0 else 0
    str_list = str_list[takes:]
    wavestr = ''
    for k in range(0, len(str_list)):
        wavestr += ('|' + str(round(str_list[k],2)))
    return wavestr



def tryBottom():
    # df = get_wave('399005', index=True)
    df = get_wave('600213')
    wave_to_str(df, size=10)
    print(df)
    bottom_def = get_bottom(df)
    print(bottom_def.ix[0, 'bottom'])
    bottom_my = get_bottom(df, limit=8)
    print(bottom_my.ix[0, 'bottom'])




if __name__ == '__main__':
    tryBottom()
    # get_wave()
    filePath = "../data/app/pa.txt"
    mystk = pd.read_csv(filePath, sep=' ')
    mystk['code'] = mystk['code'].astype('str').str.zfill(6)
    codes = list(mystk['code'])
    codes = ['000710']
    wavedflist = []
    for code in codes:
        wavedata = get_wave(code, start='2016-01-04')
        result = format_wave_data(wavedata)
        wavedflist.append(result)
        print(wavedata)

    plot_wave(wavedflist, 'wave.png')