import datetime as dt
from datetime import datetime
import pandas as pd
import numpy as np
import tushare as ts
from stocks.data import _datautils as _dt

pd.set_option('display.width', 600)

TRUMP_GENERAL='G'
TRUMP_GOLDEN='GG'
TRUMP_MARSHAL='M'
todaystr = datetime.now().strftime('%Y-%m-%d')



def get_trump(codes=None, start=None, end=None):
    starttime = datetime.now()
    if start == None:
        bwdays = dt.timedelta(-365)
        start = (starttime + bwdays).strftime("%Y-%m-%d")
    code_list = []
    if isinstance(codes, str):
        code_list.append(codes)
    else: code_list = codes

    trumpdf_list = []
    for code in code_list:
        hist_k = ts.get_k_data(code=code, start=start, end=end)
        if hist_k is None or len(hist_k) == 0:
            continue
        # latestdate = hist_k.tail(1).at[hist_k.tail(1).index.get_values()[0], 'date']
        # if todaystr != latestdate: # not the latest record
        #     # get today data from [get_realtime_quotes(code)]
        #     realtime = ts.get_realtime_quotes(code)
        #     if realtime is None or realtime.empty == True:
        #         continue
        #     todaylow = float(realtime.at[0, 'low'])
        #     if todaylow > 0:
        #         newone = {'date':todaystr,'open':float(realtime.at[0,'open']),'close':float(realtime.at[0,'price']),'high':float(realtime.at[0,'high']), 'low':todaylow,'volume':int(float(realtime.at[0,'volume'])/100),'code':code}
        #         newdf = pd.DataFrame(newone, index=[0])
        #         hist_k = hist_k.append(newdf, ignore_index=True)
        last_idx = len(hist_k.index.get_values()) - 4
        start_idx = 1
        trump_lists = []
        while start_idx <= last_idx:
            pre_k = hist_k[start_idx-1:start_idx]
            next4k = hist_k[start_idx:start_idx + 4]
            curtk = next4k.head(1)
            next3k = next4k.tail(3)

            precls = pre_k.iat[0, 2]  # close
            prevol = pre_k.iat[0, 5]  # volume

            curtdate = curtk.iat[0, 0]  # date
            curtopn = curtk.iat[0, 1]  # open
            curtcls = curtk.iat[0, 2]  # close
            curthig = curtk.iat[0, 3]  # high
            curtlow = curtk.iat[0, 4]  # low
            curtvol = curtk.iat[0, 5]  # volume
            curttop = curtcls if curtcls >= curtopn else curtopn
            curtbtm = curtopn if curtcls >= curtopn else curtcls

            next3cls = list(next3k['close'])
            next3vol = list(next3k['volume'])
            min_cls_n3k = np.min(next3k.close)
            min_opn_n3k = np.min(next3k.open)
            min_low_n3k = np.min(next3k.low)
            mean_cls_n3k = np.mean(next3k.close)

            start_idx += 1
            #multi volume appear, price raise and the next 3days min price higher than the bottom price, checkout
            if curtvol > prevol * 1.8 and curtcls > precls and curtbtm < min_cls_n3k :
                trump_list = []
                trump_price = curttop
                trump_grade = TRUMP_GENERAL

                if min_low_n3k < curttop:
                    trump_price = curtbtm

                nxt3_max_vol = np.max(next3vol)
                if (min_cls_n3k > curtcls or min_cls_n3k > curtcls * 0.99) and (nxt3_max_vol <= curtvol):
                    trump_grade = TRUMP_GOLDEN

                trump_list.append(code)
                trump_list.append(curtdate)
                trump_list.append(trump_price)
                trump_list.append(trump_grade)
                trump_lists.append(trump_list)

            # print(pre_k)
            # print(curtk)
            # print(next3k)

        trump_df = pd.DataFrame(trump_lists, columns=['code', 'date', 'price', 'grade'])
        trumpdf_list.append(trump_df)

    if trumpdf_list is None or len(trumpdf_list) == 0:
        return 'result is empty, please check the code is exist!'
    result = pd.concat(trumpdf_list, ignore_index=True)
    return result


if __name__ == '__main__':
    print('search trump...')
    codes = _dt.get_app_codes()
    result = get_trump(codes)
    _dt.to_db(result, 'trump_x')
    print(result)