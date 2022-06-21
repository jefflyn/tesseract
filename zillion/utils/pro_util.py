import tushare as ts

token = '99dec24a97c268cac40c0761443d2ceaa2ae4089949c65d61630b3fe'
ts.set_token(token)

pro = ts.pro_api()


def heart_beat_0264():
    token_0264 = 'a2da74fb9a93e682f592c2a64081b6ac874230b6a499f29faee7a30a'
    pro_0264 = ts.pro_api(token_0264)
    df = pro_0264.trade_cal(exchange='', start_date='20200602', end_date='20201231',
                            fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
    print(df)
    df = pro_0264.query('trade_cal', exchange='', start_date='20200602', end_date='20201231',
                        fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
    print(df)


def heart_beat_ljg123():
    token_ljg123 = '00493a4232932367d119f9d0e2ad4b8ad5ac0960f0d0556504a6bbdc'
    pro_ljg123 = ts.pro_api(token_ljg123)
    df = pro_ljg123.trade_cal(exchange='', start_date='20200602', end_date='20201231',
                            fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
    print(df)
    df = pro_ljg123.query('trade_cal', exchange='', start_date='20200602', end_date='20201231',
                        fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
    print(df)


if __name__ == '__main__':
    heart_beat_0264()
    heart_beat_ljg123()

