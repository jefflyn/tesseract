import tushare as ts
import time
import datetime

from stocks.util import sms_util
from stocks.util.redis_util import redis_client
from stocks.data import data_util


pre_key_today = data_util.TODAY + '_'


if __name__ == '__main__':
    """
    nohup /usr/local/bin/redis-server /etc/redis.conf &
    """
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

            realtime_price_info = str(price) + ' ' + str(round(realtime_change, 2)) + '%'
            print(' ', code, realtime_price_info, str(alert_prices), str(alert_changes), sep=' | ')

            if prices is None and prices != '':
                for p in prices:
                    target_price = float(p)
                    if 0 < target_price <= price:
                        redis_key = pre_key_today + code + '_price_' + str(target_price)
                        warn_times = redis_client.get(redis_key)
                        if warn_times is None:
                            content = name + ':' + code + ' up to ' + str(target_price) + ', please check!'
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
                    if target_price < 0 and price <= abs(target_price):
                        redis_key = pre_key_today + code + '_price_' + abs(target_price)
                        warn_times = redis_client.get(redis_key)
                        if warn_times is None:
                            content = name + ':' + code + ' down to ' + str(abs(target_price)) + ', please check!'
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
