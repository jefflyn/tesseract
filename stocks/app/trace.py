import tushare as ts
import pandas as pd
import time
import datetime

pd.set_option('display.width',600)

simdf = pd.read_csv("./data/trace.txt", sep=' ')
simdf['code'] = simdf['code'].astype('str').str.zfill(6)

codes = list(simdf['code'])
print(len(codes))

df = ts.get_realtime_quotes(codes)
data_list = []
for index,row in df.iterrows() :
    code = row['code']
    pre_close = float(row['pre_close'])
    price = float(row['price'])
    price_diff = price - pre_close
    change_percent = price_diff / pre_close * 100
    
    index = list(simdf['code']).index(code)
    cost = simdf.ix[index,'cost']
    share = simdf.ix[index,'share']
    cost_diff = price - cost
    profit = (cost_diff) * share
    profit_percent = cost_diff / cost * 100.0
	  
    datastr = str("%.3f%%"%change_percent) + ',' + str("%.2f"%cost_diff) + ',' + str("%.2f"%profit) + ',' + str("%.3f"%profit_percent)
    data_list.append([astr for astr in datastr.split(',')])
    df_append = pd.DataFrame(data_list, columns=['change_percent','cost_diff','profit','profit_percent'])

df = df.join(df_append)
df['profit_percent'] = df['profit_percent'].astype('float32')
df = df.sort_values('profit_percent', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')

df['profit_percent'] = df['profit_percent'].apply(lambda x : str(round(x,3)) + '%')
print(df[['code','name','price','change_percent','cost_diff','profit','profit_percent']])
# print(df[['code','name','price','change_percent','bid','ask','pre_close','open','low','high','time','cost_diff','profit','profit_percent']])
