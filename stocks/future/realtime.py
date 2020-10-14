import time
from sys import argv

import pandas as pd
import requests

from stocks.future import future_util
from stocks.util import date_util
from stocks.util import db_util
from stocks.util import notify_util
from stocks.util import sms_util, date_const
from stocks.util.redis_util import redis_client

MONITOR_SYMBOL_MAP = {
    '鲜苹果2101': [-7880, -7885, -7890, -7895, -7900, -7905, -7910, -7915],
    '棉花2101': [-13900, -13925, -13950, -13975, -14000, -14025, -14050, -14100]
}


def notify_trigger(symbol=None, price=None, change=None, alert=True):
    '''
    手动设置提醒告警条件
    :param symbol:
    :param price:
    :param change:
    :param alert:
    :return:
    '''
    symbol_list = MONITOR_SYMBOL_MAP.keys()
    if symbol is not None and symbol in symbol_list:
        msg_content = symbol + '到达' + str(price)
        target_prices = MONITOR_SYMBOL_MAP.get(symbol)
        if price in target_prices:
            notify_util.notify(content=msg_content)
        if alert:
            if target_prices[0] < 0:
                if price <= abs(target_prices[0]) or price <= abs(target_prices[len(target_prices) - 3]):
                    notify_util.alert(message=msg_content)
            else:
                if price <= target_prices[0] or price >= target_prices[len(target_prices) - 3]:
                    notify_util.alert(message=msg_content)


def format_realtime(df):
    # format data
    df['low'] = df['low'].apply(lambda x: '_' + str(round(float(x), 2)))
    df['high'] = df['high'].apply(lambda x: '^' + str(round(float(x), 2)))
    df['change'] = df['change'].apply(lambda x: str(round(x, 2)) + '%')
    df['position'] = df['position'].apply(lambda x: str(round(x, 2)) + '%')
    df['limit'] = df['limit'].apply(lambda x: str(round(x, 2)) + '%')
    df['one_value'] = df['one_value'].apply(lambda x: '[' + str(x) + ',')
    df['one_margin'] = df['one_margin'].apply(lambda x: str(x) + ',')
    df['onem_margin'] = df['onem_margin'].apply(lambda x: str(x) + ']')

    return df


def re_exe(interval=10, sortby=None):
    """
    http://hq.sinajs.cn/list=EB0,IC0,IF0,IH0,LU0,NR0,PG0,PM0,RR0,SA0,SS0,T0,TF0,TS0,UR0
    :param interval:
    :param sortby:
    :return:
    """
    on_target = (sortby == 'c')

    while True:
        future_basics = future_util.get_future_basics(on_target=on_target)
        future_name_list = list(future_basics['name'])
        codes = ','.join(list(future_basics['symbol']))
        req_url = 'http://hq.sinajs.cn/list='
        future_from_sina = []
        result = requests.get(req_url + codes)
        txt = result.text
        # print(txt)
        if txt is not None and len(txt.split(';')) > 0:
            groups = txt.split(';\n')
            result_list = []
            for content in groups:
                if len(content) == 0:
                    continue
                info = content.split('=')[1].replace('"', '').strip().split(',')
                if len(info) < 18:
                    continue
                name = info[0]  # 0：名字
                # 1：不明数字
                open = float(info[2])  # 2：开盘价
                high = float(info[3])  # 3：最高价
                # 4：最低价
                low = float(info[4])
                # 5：昨日收盘价
                pre_close = float(info[5])
                # 6：买价，即“买一”报价
                bid = float(info[6])
                # 7：卖价，即“卖一”报价
                ask = float(info[7])
                # 8：最新价，即收盘价
                price = float(info[8])
                # 9：结算价
                settle = float(info[9])
                # 10：昨结算
                pre_settle = float(info[10])
                # 11：买量
                # 12：卖量
                # 13：持仓量
                # 14：成交量
                # 15：商品交易所简称
                exchange = info[15]
                # 16：品种名简称
                alias = info[16]
                # 17：日期
                trade_date = info[17]
                future_from_sina.append(alias)
                # print(alias)
                # 清除可以查询的商品
                for goods_name in future_name_list:
                    if goods_name.startswith(alias):
                        future_name_list.remove(goods_name)

                target_df = future_basics.loc[future_basics['name'].str.contains(alias)]
                if target_df.empty:
                    print(name, alias, 'empty')
                for index, row in target_df.iterrows():
                    amount_per_contract = row['amount']
                    limit_in = row['limit']
                    margin_rate = row['margin_rate']
                    alert_prices = target_df.loc[index, 'alert_price']
                    alert_changes = target_df.loc[index, 'alert_change']
                    receive_mobile = target_df.loc[index, 'alert_mobile']
                    prices = str.split(alert_prices, ',') if alert_prices is not None else None
                    changes = str.split(alert_changes, ',') if alert_changes is not None and alert_changes != '' \
                        else None
                value_per_contract = round(float(price) * amount_per_contract, 2)
                margin_per_contract = round(value_per_contract * margin_rate / 100, 2)
                try:
                    contract_num_for_1m = int(1000000 / value_per_contract) + 1
                    margin_for_1m = round(contract_num_for_1m * value_per_contract * margin_rate / 100, 2)
                except:
                    print(name, "数据有误:", info)

                price_diff = float(price) - float(pre_settle)
                change = round(price_diff / float(pre_settle) * 100, 2)
                position = 0
                if high != low:
                    position = round((price - low) / (high - low) * 100, 2)
                elif high == low > price:
                    position = 100

                realtime_change_str = '+' + str(round(change, 2)) if change > 0 else str(round(change, 2))
                realtime_price_info = str(price) + ' ' + realtime_change_str + '%'
                # print(' ', name, realtime_price_info, str(alert_prices), str(alert_changes), sep=' | ')
                alert_trigger(symbol=name, realtime_price=price, prices=prices, realtime_change=change, changes=changes)
                notify_trigger(symbol=name, price=price, change=change, alert=True)

                row_list = [name, alias, exchange, price, change, limit_in, bid, ask, low, high, round(position, 2),
                            value_per_contract, margin_per_contract, str(contract_num_for_1m) + '-' + str(margin_for_1m),
                            trade_date, date_util.get_now()]
                result_list.append(row_list)
            df = pd.DataFrame(result_list, columns=['name', 'alias', 'exchange', 'price', 'change', 'limit',
                                                    'bid1', 'ask1', 'low', 'high', 'position',
                                                    'one_value', 'one_margin', 'onem_margin', 'date', 'time'])
            if sortby == 'p':
                df = df.sort_values(['position'], ascending=False)
            else:
                df = df.sort_values(['change'])

            db_util.to_db(df, tbname='future_realtime')

            final_df = format_realtime(df)
            if final_df.empty:
                print('no data, exit!')
                break
            print(final_df)
            # print(future_from_sina, '可查')
            print(tuple(future_name_list), '查无结果!')
            time.sleep(interval)


def alert_trigger(symbol=None, realtime_price=None, prices=None, realtime_change=None, changes=None, receive_mobile='18507550586'):
    if prices is not None and prices != '':
        for p in prices:
            if p == '':
                continue
            target_price = round(float(p), 0)
            if 0 < target_price <= realtime_price:
                redis_key = date_util.get_today() + symbol + '_price_' + str(target_price)
                warn_times = redis_client.get(redis_key)
                if warn_times is None:
                    try:
                        redis_client.set(redis_key, symbol + str(realtime_price), ex=date_const.ONE_MONTH * 3)
                        name_format = '：' + symbol
                        change_str = str(round(realtime_change, 2)) + '%' if realtime_change < 0 else '+' + str(
                            round(realtime_change, 2)) + '%'
                        price_format = str(round(realtime_price)) + ' ' + change_str
                        # send msg
                        t_msg = sms_util.send_msg_with_tencent(name=name_format, price=price_format, to=receive_mobile)
                        print(t_msg)
                    except Exception as e:
                        print(e)
            if target_price < 0 and realtime_price <= abs(target_price):
                redis_key = date_util.get_today() + symbol + '_price_' + str(abs(target_price))
                warn_times = redis_client.get(redis_key)
                if warn_times is None:
                    try:
                        redis_client.set(redis_key, symbol + str(realtime_price), ex=date_const.ONE_MONTH * 3)
                        name_format = '：' + symbol
                        change_str = str(round(realtime_change, 2)) + '%' if realtime_change < 0 else '+' + str(
                            round(realtime_change, 2)) + '%'
                        price_format = str(round(realtime_price)) + ' ' + change_str
                        # send msg
                        t_msg = sms_util.send_msg_with_tencent(name=name_format, price=price_format, to=receive_mobile)
                        print(t_msg)
                    except Exception as e:
                        print(e)

    if changes is not None and changes != '':
        for p in changes:
            if p == '':
                continue
            redis_key = date_util.get_today() + symbol + '_change_' + p
            warn_times = redis_client.get(redis_key)
            if 0 < float(p) <= realtime_change:
                if warn_times is None:
                    value = symbol + ':' + str(realtime_price) + ' +' + str(round(realtime_change, 2)) + '%'
                    try:
                        redis_client.set(redis_key, value, ex=date_const.ONE_MONTH * 3)
                        name_format = '：' + symbol
                        change_str = str(round(realtime_change, 2)) + '%' if realtime_change < 0 else '+' + str(
                            round(realtime_change, 2)) + '%'
                        price_format = str(round(realtime_price)) + ' ' + change_str
                        # send msg
                        t_msg = sms_util.send_msg_with_tencent(name=name_format, price=price_format, to=receive_mobile)
                        print(t_msg)
                    except Exception as e:
                        print(e)

            if 0 > float(p) >= realtime_change >= -20:
                if warn_times is None:
                    value = symbol + ' ' + str(realtime_price) + ' ' + str(round(realtime_change, 2)) + '%'
                    try:
                        redis_client.set(redis_key, value, ex=date_const.ONE_MONTH * 3)
                        name_format = '：' + code + ' ' + name
                        change_str = str(round(realtime_change, 2)) + '%' if realtime_change < 0 else '+' + str(
                            round(realtime_change, 2)) + '%'
                        price_format = str(round(realtime_price)) + ' ' + change_str
                        # send msg
                        t_msg = sms_util.send_msg_with_tencent(name=name_format, price=price_format, to=receive_mobile)
                        print(t_msg)
                    except Exception as e:
                        print(e)


if __name__ == '__main__':
    """
    python realtime.py argv1 argv2[c|p]
    nohup /usr/local/bin/redis-server /usr/local/etc/redis.conf &
    nohup /usr/local/bin/redis-server /etc/redis.conf &
    """
    # if len(argv) > 1:
    #     type = argv[1]
    #     if type not in KEYS:
    #         print("Contract Type NOT defined. Try the followings: " + str(KEYS))
    #         sys.exit(0)
    # else:
    #     type = 'my'
    #
    if len(argv) > 1 and argv[1] in ['a', 'c', 'p']:
        sort = argv[1]
    else:
        sort = 'c'
    re_exe(5, sortby=sort)
