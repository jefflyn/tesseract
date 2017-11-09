
# coding: utf-8
import sys
from sys import argv
import tushare as ts
import pandas as pd
import time

if len(argv) < 2:
        print("Invalid args! At least 2 args like: python xxx.py arg1 ...")
        sys.exit(0)
file = argv[1]
include_files = {
        'pa': './data/pa.txt',
        'cf': './data/cf.txt',
        'other': './data/other.txt'
        }
keys = list(include_files.keys())
if file not in keys:
        print("File name NOT found. Try the followings: " + str(keys))
        sys.exit(0)

filePath = include_files[file]
        
pd.set_option('display.max_rows',50)
pd.set_option('display.max_columns',80)
pd.set_option('display.width',600)

hddf = pd.read_csv(filePath, sep=' ')
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
	      warn_sign = '***' 
	    elif esc_diff < 0 :
	      warn_sign = '!!!'
	    
	    datastr = warn_sign + ',' + str("%.3f"%change) + ',' + str("[%.3f%%]"%change) + ',' + str("[%.3f"%cost_diff) + ',' + str("%.3f"%profit) + ',' + str("%.3f%%]"%profit_perc) + ',' + str("[%.3f"%bottom) + ',' + str("%.3f"%escape) + ',' + str("%.3f%%]"%btm_space) + ',' + str("%.3f%%"%esc_space)
	    data_list.append([astr for astr in datastr.split(',')])
	
	    df_append = pd.DataFrame(data_list, columns=['warn','change1','change','cost_diff','profit_amt','profit_perc','btm_diff','esc_diff','btm_space','esc_space'])
	  
	  
	  df = df.join(df_append)
	  
	  df['change1'] = df['change1'].astype('float32')
	  df = df.sort_values('change1', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
	  ##df.rename(columns={'name':'stock_name'}, inplace = True)
	  ##print(df[['code','name','price','change','bid','ask','pre_close','open','low','high','time','cost_diff','profit','profit_percent']])
	  print(df[['warn','code','name','price','change','bid','ask','low','high','btm_diff','btm_space','esc_diff','esc_space','cost_diff','profit_amt','profit_perc']])
	  
	  time.sleep(inc)
    

re_exe(3)





