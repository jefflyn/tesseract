import tushare as ts

token = 'f65316bb26b0a27ef7f876249615fcba99b5aab10e5be46cb278e53e'
ts.set_token(token)
pro = ts.pro_api()


if __name__ == '__main__':
    # 设置你的token
    df = pro.user(token=token)
    print(df)
    df_data = pro.fut_daily(ts_code='BR2403.SHF')
