import tushare as ts
import time
import datetime

from stocks.base import sms_util
from stocks.base.redis_util import redis_client
from stocks.data import data_util
from stocks.base import date_const


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
            name = monitor_stocks.ix[index, 'name']
            up_price_triggers = monitor_stocks.ix[index, 'price_up']
            down_price_triggers = monitor_stocks.ix[index, 'price_down']
            change_triggers = monitor_stocks.ix[index, 'change_percent']
            receive_mobile = monitor_stocks.ix[index, 'receive_mobile']

            up_prices = str.split(up_price_triggers, ',')
            down_prices = str.split(down_price_triggers, ',')
            changes = str.split(change_triggers, ',')

            for p in up_prices:
                if price >= float(p):
                    redis_key = pre_key_today + code + '_price_' + p
                    warn_times = redis_client.get(redis_key)
                    if warn_times is None:
                        content = name + ': ' + code + ' up to ' + p + ', please check!'
                        try:
                            redis_client.set(redis_key, name + str(price))
                            sms_util.message_to(msg=content, to=receive_mobile)
                            print(content)
                        except Exception as e:
                            print(e)

            for p in down_prices:
                if price <= float(p):
                    redis_key = pre_key_today + code + '_price_' + p
                    warn_times = redis_client.get(redis_key)
                    if warn_times is None:
                        content = name + ': ' + code + ' down to ' + p + ', please check!'
                        try:
                            redis_client.set(redis_key, name + str(price))
                            sms_util.message_to(msg=content, to=receive_mobile)
                            print(content)
                        except Exception as e:
                            print(e)

            for p in changes:
                if float(p) > 0 and realtime_change >= float(p):
                    redis_key = pre_key_today + code + '_change_' + p
                    warn_times = redis_client.get(redis_key)
                    if warn_times is None:
                        content = name + ' ' + code + ' change to +' + p + '%, please check!'
                        value = name + ': ' + str(price) + ' +' + str(round(realtime_change, 2)) + '%'
                        try:
                            redis_client.set(redis_key, value)
                            sms_util.message_to(msg=content, to=receive_mobile)
                            print(content)
                        except Exception as e:
                            print(e)

                if float(p) < 0 and realtime_change <= float(p):
                    redis_key = pre_key_today + code + '_change_' + p
                    warn_times = redis_client.get(redis_key)
                    if warn_times is None:
                        content = name + ': ' + code + ' change to ' + p + '%, please check!'
                        value = name + ' ' + str(price) + ' ' + str(round(realtime_change, 2)) + '%'
                        try:
                            redis_client.set(redis_key, value)
                            sms_util.message_to(msg=content, to=receive_mobile)
                            print(content)
                        except Exception as e:
                            print(e)
        print(str(datetime.datetime.now()) + ' >>> keep eyes on ... total: ' + str(len(codes)))
        time.sleep(3)
