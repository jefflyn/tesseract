import tushare as ts
import time
import datetime

from stocks.base import sms_util
from stocks.base.redis_util import redis_client
from stocks.data import data_util
from stocks.base import date_const


pre_key_today = date_const.TODAY + '_'


if __name__ == '__main__':
    monitor_stocks = data_util.get_monitor_stocks()
    codes = list(monitor_stocks['code'])
    while True:
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
            alias = monitor_stocks.ix[index, 'alias']
            up_price_triggers = monitor_stocks.ix[index, 'price_up']
            down_price_triggers = monitor_stocks.ix[index, 'price_down']
            change_triggers = monitor_stocks.ix[index, 'change_percent']

            up_prices = str.split(up_price_triggers, ',')
            down_prices = str.split(down_price_triggers, ',')
            changes = str.split(change_triggers, ',')

            for p in up_prices:
                if price >= float(p):
                    warn_times = redis_client.get(pre_key_today + code)
                    if warn_times is None:
                        content = alias + ': ' + code + ' up to ' + p + ', please check!'
                        sms_util.message_to(msg=content, to='+8618507550586')
                        redis_client.set(pre_key_today + code, alias + str(price))
                        print(content)

            for p in down_prices:
                if price <= float(p):
                    warn_times = redis_client.get(pre_key_today + code)
                    if warn_times is None:
                        content = alias + ': ' + code + ' down to ' + p + ', please check!'
                        sms_util.message_to(msg=content, to='+8618507550586')
                        redis_client.set(pre_key_today + code, alias + str(price))
                        print(content)

            for p in changes:
                if float(p) > 0 and realtime_change >= float(p):
                    warn_times = redis_client.get(pre_key_today + code + '_change')
                    if warn_times is None:
                        content = alias + ' ' + code + ' change to +' + p + '%, please check!'
                        sms_util.message_to(msg=content, to='+8618507550586')
                        value = alias + ': ' + str(price) + ' +' + str(round(realtime_change, 2)) + '%'
                        redis_client.set(pre_key_today + code + '_change', value)
                        print(content)

                if float(p) < 0 and realtime_change <= float(p):
                    warn_times = redis_client.get(pre_key_today + code + '_change')
                    if warn_times is None:
                        content = alias + ': ' + code + ' change to ' + p + '%, please check!'
                        sms_util.message_to(msg=content, to='+8618507550586')
                        value = alias + ' ' + str(price) + ' -' + str(round(realtime_change, 2)) + '%'
                        redis_client.set(pre_key_today + code + '_change', value)
                        print(content)
        print(str(datetime.datetime.now()) + ' >>> keep eyes on ...')
        time.sleep(3)
