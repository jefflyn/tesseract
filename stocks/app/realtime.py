import sys
from sys import argv
import tushare as ts
from tushare.stock import cons as ct
import pandas as pd
import time

pd.set_option('display.width',800)

if len(argv) < 2:
        print("Invalid args! At least 2 args like: python xxx.py arg1 ...")
        sys.exit(0)
file = argv[1]
include_files = {
        'pa': './data/pa.txt',
        'cf': './data/cf.txt',
        'idx': './data/idx.txt',
        'other': './data/other.txt'
        }
keys = list(include_files.keys())
if file not in keys:
        print("File name NOT found. Try the followings: " + str(keys))
        sys.exit(0)

filePath = include_files[file]
hddf = pd.read_csv(filePath, sep=' ')
if file != 'idx' :
  hddf['code'] = hddf['code'].astype('str').str.zfill(6)
codes = list(hddf['code'])

INDEX_LIST_NEW = dict(zip(list(x[2:] for x in ct.INDEX_LIST.values()), ct.INDEX_LIST.keys()))

def re_exe(inc = 3) :
    while True:
        df = ts.get_realtime_quotes(codes)
        data_list = []
        for index,row in df.iterrows() :
            code = row['code']

            code = INDEX_LIST_NEW[code] if code in INDEX_LIST_NEW.keys() else code

            pre_close = float(row['pre_close'])
            price = float(row['price'])

            price_diff = price - pre_close
            change = price_diff / pre_close * 100

            index = list(hddf['code']).index(code)
            cost = hddf.ix[index,'cost']
            share = hddf.ix[index,'share']
            bottom = hddf.ix[index,'bottom']
            escape = hddf.ix[index,'escape']

            cost_diff = price - cost
            profit = (cost_diff) * share

            if profit < 0 and price > 0:
                profit_perc = (cost / price - 1) * -100.0
            else :
                profit_perc = cost_diff / cost * 100.0

            ##calculate the bottom, the smaller the possibility of bounce is bigger.
            ##if negative, that means the bottom is broken, pay much attention if get out or wait for the escape line
            btm_diff = price - bottom
            esc_diff = (price - escape) if (btm_diff < 0) else (bottom - escape)

            btm_space = btm_diff / bottom * 100.0
            esc_space = esc_diff / escape * 100.0

            warn_sign = ''
            if profit > 0 :
              warn_sign = '$$$'
            elif btm_diff <= 0 :
              warn_sign = '!!!'

            #datastr = warn_sign + ',' + str("%.3f"%change) + ',' + str("[%.3f%%]"%change) + ',' + str("[%.3f"%cost_diff) + ',' + str("%.3f"%profit) + ',' + str("%.3f"%profit_perc) + ',' + str("%.3f%%]"%profit_perc) + ',' + str("[%.3f"%bottom) + ',' + str("%.3f"%escape) + ',' + str("%.3f%%]"%btm_space) + ',' + str("%.3f%%"%esc_space)
            #data_list.append([astr for astr in datastr.split(',')])
            #df_append = pd.DataFrame(data_list, columns=['warn','change1','change','cost_diff','profit_amt','profit_p','profit_perc','btm_diff','esc_diff','btm_space','esc_space'])

            curt_data = []
            curt_data.append(warn_sign)
            curt_data.append(change)
            curt_data.append(cost_diff)
            curt_data.append(profit)
            curt_data.append(profit_perc)
            curt_data.append(btm_diff)
            curt_data.append(esc_diff)
            curt_data.append(btm_space)
            curt_data.append(esc_space)
            curt_data.append(price * share)
            data_list.append(curt_data)

        df_append = pd.DataFrame(data_list, columns=['warn','change','cost_diff','profit_amt','profit_perc','btm_diff','esc_diff','btm_space','esc_space','total_amt'])
        df = df.join(df_append)

        # df['change'] = df['change'].astype('float32')
        # df['profit_perc'] = df['profit_perc'].astype('float32')
        if len(argv) > 2 and argv[2] == 'p':
          df = df.sort_values('profit_perc', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
        elif len(argv) > 2 and argv[2] == 'b':
          df = df.sort_values('btm_space', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
        else:
          df = df.sort_values('change', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')

        #format data
        df['change'] = df['change'].apply(lambda x : str(round(x,3)) + '%')
        df['profit_perc'] = df['profit_perc'].apply(lambda x: str(round(x, 3)) + '%')
        df['btm_space'] = df['btm_space'].apply(lambda x: str(round(x, 3)) + '%')
        df['esc_space'] = df['esc_space'].apply(lambda x: str(round(x, 3)) + '%')

        print(df[['warn','code','name','price','change','bid','ask','low','high','btm_diff','btm_space','esc_diff','esc_space','cost_diff','profit_amt','profit_perc','total_amt']])

        time.sleep(inc)

re_exe(3)





