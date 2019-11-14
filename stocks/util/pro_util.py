import tushare as ts

token = 'f65316bb26b0a27ef7f876249615fcba99b5aab10e5be46cb278e53e'
ts.set_token(token)

pro = ts.pro_api()

# pro = ts.pro_api(token)
# df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
# print(df)
# df = pro.query('trade_cal', exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
# print(df)