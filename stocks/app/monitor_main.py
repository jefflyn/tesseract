import tushare as ts
import time
import datetime

from stocks.util import sms_util
from stocks.util.redis_util import redis_client
from stocks.data import data_util
from stocks.util import date_const


pre_key_today = date_const.TODAY + '_'


if __name__ == '__main__':
    while True:
        monitor_stocks = data_util.get_monitor_stocks()
        codes = list(monitor_stocks['code'])
        realtime_df = ts.get_realtime_quotes(codes)
        data_list = []
        for index, row in realtime_df.iterrows():
            code = row['code']
            pre_close = float(row['pre_close'])
            price = float(row['price'])
            low = float(row['low'])
            price_diff = price - pre_close
            realtime_change = price_diff / pre_close * 100

            index = list(monitor_stocks['code']).index(code)
            name = monitor_stocks.loc[index, 'name']
            alert_prices = monitor_stocks.loc[index, 'alert_price']
            alert_changes = monitor_stocks.loc[index, 'percent_change']
            receive_mobile = monitor_stocks.loc[index, 'receive_mobile']

            prices = str.split(alert_prices, ',')
            changes = str.split(alert_changes, ',')

            for p in prices:
                if price == float(p):
                    redis_key = pre_key_today + code + '_price_' + p
                    warn_times = redis_client.get(redis_key)
                    if warn_times is None:
                        content = name + ':' + code + ' up to ' + p + ', please check!'
                        try:
                            redis_client.set(redis_key, name + str(price))
                            name_format = '：' + code + ' ' + name
                            change_str = str(round(realtime_change, 2)) + '%' if realtime_change < 0 else '+' + str(
                                round(realtime_change, 2)) + '%'
                            price_format = str(round(price, 2)) + change_str
                            # send msg
                            # t_msg = sms_util.send_msg_with_twilio(msg=content, to=receive_mobile)
                            t_msg = sms_util.send_msg_with_tencent(code, name_format, price_format)
                            print(t_msg)
                        except Exception as e:
                            print(e)

            for p in changes:
                if 0 < float(p) <= realtime_change:
                    redis_key = pre_key_today + code + '_change_' + p
                    warn_times = redis_client.get(redis_key)
                    if warn_times is None:
                        content = name + ' ' + code + ' change to +' + p + '%, please check!'
                        value = name + ':' + str(price) + ' +' + str(round(realtime_change, 2)) + '%'
                        try:
                            redis_client.set(redis_key, value)
                            name_format = '：' + code + ' ' + name
                            change_str = str(round(realtime_change, 2)) + '%' if realtime_change < 0 else '+' + str(
                                round(realtime_change, 2)) + '%'
                            price_format = str(round(price, 2)) + change_str
                            # send msg
                            # t_msg = sms_util.send_msg_with_twilio(msg=content, to=receive_mobile)
                            t_msg = sms_util.send_msg_with_tencent(code, name_format, price_format)
                            print(t_msg)
                        except Exception as e:
                            print(e)

                if 0 > float(p) >= realtime_change:
                    redis_key = pre_key_today + code + '_change_' + p
                    warn_times = redis_client.get(redis_key)
                    if warn_times is None:
                        content = name + ':' + code + ' change to ' + p + '%, please check!'
                        value = name + ' ' + str(price) + ' ' + str(round(realtime_change, 2)) + '%'
                        try:
                            redis_client.set(redis_key, value)
                            name_format = '：' + code + ' ' + name
                            change_str = str(round(realtime_change, 2)) + '%' if realtime_change < 0 else '+' + str(
                                round(realtime_change, 2)) + '%'
                            price_format = str(round(price, 2)) + change_str
                            # send msg
                            # t_msg = sms_util.send_msg_with_twilio(msg=content, to=receive_mobile)
                            t_msg = sms_util.send_msg_with_tencent(code, name_format, price_format)
                            print(t_msg)
                        except Exception as e:
                            print(e)
        print(str(datetime.datetime.now()) + ' >>> keep eyes on ... total: ' + str(len(codes)))
        time.sleep(3)
