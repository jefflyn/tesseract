
# coding: utf-8

import tushare as ts
import pandas as pd
import time

pd.set_option('display.max_rows',50)
pd.set_option('display.max_columns',80)
pd.set_option('display.width',600)

hddf = pd.read_csv("./others.txt", sep=' ')
codes = list(hddf['code'])

def re_exe(inc = 3) :
	while True: 
	  df = ts.get_realtime_quotes(codes)
	  data_list = []
	  for index,row in df.iterrows() :
	    code = row['code'] if row['code'] not in ['000001'] else 'sh'
	    #print(code)
	    pre_close = float(row['pre_close'])
	    price = float(row['price'])
	
	    price_diff = price - pre_close
	    change_percent = price_diff / pre_close * 100
	
	    index = list(hddf['code']).index(code)
	    cost = hddf.ix[index,'cost']
	    share = hddf.ix[index,'share']
	
	    cost_diff = price - cost
	    profit = (cost_diff) * share
	    if profit < 0 and price > 0:
	    	profit_percent = (cost / price - 1) * -100.0
	    else : 
	    	profit_percent = cost_diff / cost * 100.0
	
	    datastr = str("%.3f"%change_percent) + ',' + str("%.3f"%cost_diff) + ',' + str("%.3f"%profit) + ',' + str("%.3f%%"%profit_percent)
	    data_list.append([astr for astr in datastr.split(',')])
	
	    df_append = pd.DataFrame(data_list, columns=['change_percent','cost_diff','profit','profit_percent'])
	  
	  
	  df = df.join(df_append)
	  
	  df['change_percent'] = df['change_percent'].astype('float32')
	  df = df.sort_values('change_percent', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
	
	  print(df[['code','name','price','change_percent','bid','ask','pre_close','open','low','high','time','cost_diff','profit','profit_percent']])
	  
	  time.sleep(inc)
    

re_exe(3)





