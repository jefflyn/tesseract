# coding: utf-8

import tushare as ts
import pandas as pd
import time

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 80)
pd.set_option('display.width', 600)

hddf = pd.read_csv("./data/monitor_gap.txt", sep=' ')
hddf['code'] = hddf['code'].astype('str').str.zfill(6)
codes = list(hddf['code'])

basics = pd.read_csv("../data/basics.csv", sep=",", encoding="gbk")
basics['code'] = basics['code'].astype('str').str.zfill(6)

def re_exe(inc=3):
    while True:
        df = ts.get_realtime_quotes(codes)
        data_list = []
        for index, row in df.iterrows():
            code = row['code'] if row['code'] not in ['000001'] else 'sh'

            info = basics[basics['code'].astype(object) == code]
            industry = info['industry']
            area = info['area']
            pe = info['pe']

            # print(code)
            pre_close = float(row['pre_close'])
            price = float(row['price'])
            low = float(row['low'])

            price_diff = price - pre_close
            change = price_diff / pre_close * 100

            index = list(hddf['code']).index(code)
            
            bottom = hddf.ix[index, 'bottom']
            escape = hddf.ix[index, 'escape']

            ##calculate the bottom, the smaller the possibility of bounce is bigger.
            ##if negative, that means the bottom is broken, pay much attention if get out or wait for the escape line
            btm_diff = price - bottom
            esc_diff = (price - escape) if (btm_diff < 0) else (bottom - escape)

            btm_space = btm_diff / bottom * 100.0
            esc_space = esc_diff / escape * 100.0

            warn_sign = ''
            if btm_diff <= 0:
                warn_sign = '***'
            
            if esc_diff < 0 or (escape >= low):
                warn_sign = '!!!'

            datastr = warn_sign + ',' + str("%.3f" % change) + ',' + str("[%.3f]" % bottom) + ',' + str("%.3f" % escape) + ',' \
                      + str("%.3f%%]" % btm_space) + ',' + str("%.3f" % btm_space) + ',' + str("%.3f%%" % esc_space)
            print (datastr)
            data_list.append([astr for astr in datastr.split(',')])

            df_append = pd.DataFrame(data_list, columns=['warn', 'change', 'btm_diff', 'esc_diff', 'btm_space', 'btm_perc', 'esc_space'])
            df_append['industry'] = info['industry']
            df_append['area'] = info['area']
            df_append['pe'] = info['pe']

        df = df.join(df_append)
        df['btm_perc'] = df['btm_perc'].astype('float32')
        df = df.sort_values('btm_perc', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
        
        print(df[['warn', 'code', 'name', 'change', 'price', 'low', 'btm_diff', 'btm_space', 'esc_diff', 'esc_space','industry','area','pe']])

        time.sleep(inc)

re_exe(3)
