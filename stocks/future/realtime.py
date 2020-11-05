import time
from sys import argv

import pandas as pd
import requests

from stocks.future import future_util
from stocks.util import date_util
from stocks.util import db_util
from stocks.util import notify_util
from stocks.util import sms_util, date_const
from stocks.util.db_util import get_db
from stocks.util.redis_util import redis_client

group_list = ['d', 'all', 'ag', 'om', 'ch', 'co', 'en', 'pm', 'fm', 'nfm', 'fi']


def notify_trigger(symbol=None, price=None, alert_prices=None, alert=True):
    '''
    手动设置提醒告警条件
    :param alert_prices:
    :param symbol:
    :param price:
    :param change:
    :param alert:
    :return:
    '''
    if alert_prices is None or len(alert_prices) == 0:
        return
    if symbol is not None:
        msg_content = symbol + '到达' + str(price)
        notify_prices = [abs(float(e)) for e in alert_prices if e != '']
        target_price_len = len(notify_prices)
        if target_price_len < 2:
            # notify_util.notify(content=symbol + ':价格设置至少[2个]')
            print('⚠️' + symbol + ':价格设置至少[2个]')
            return

        if price in notify_prices:
            notify_util.notify(content=msg_content)
        if alert:
            first_price = float(alert_prices[0])
            before_last_price = float(alert_prices[target_price_len - 2])
            last_price = float(alert_prices[target_price_len - 1])

            # 做空方向
            if first_price < 0:
                if price <= abs(first_price) or price <= abs(before_last_price) or price >= abs(last_price):
                    notify_util.alert(message=msg_content)
            else:
                if price >= first_price or price >= abs(before_last_price) or price <= abs(last_price):
                    notify_util.alert(message=msg_content)


def format_realtime(df):
    # format data
    df['low'] = df['low'].apply(lambda x: '_' + str(round(float(x), 2)))
    df['high'] = df['high'].apply(lambda x: '^' + str(round(float(x), 2)))
    df['change'] = df['change'].apply(lambda x: str(round(x, 2)) + '%')
    df['position'] = df['position'].apply(lambda x: 'p-' + str(round(x, 2)) + '%')
    df['limit'] = df['limit'].apply(lambda x: '^' + str(round(x, 2)) + '%')
    df['one_value'] = df['one_value'].apply(lambda x: '[' + str(x) + ',')
    df['one_margin'] = df['one_margin'].apply(lambda x: str(x) + ',')
    df['onem_margin'] = df['onem_margin'].apply(lambda x: str(x) + ']')

    return df


def re_exe(interval=10, group_type=None):
    """
    http://hq.sinajs.cn/list=nf_SA2101
    :param interval:
    :param group_type:
    :return:
    """
    on_target = (group_type is None or group_type == 'd')
    # 建立数据库连接
    db = get_db()
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()

    while True:
        future_basics = future_util.get_future_basics(type=group_type, on_target=on_target)
        future_name_list = list(future_basics['name'])
        codes = ','.join(['nf_' + e for e in list(future_basics['symbol'])])
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
                # 0：名字
                name = info[0]
                # 1：不明数字
                # 2：开盘价
                open = float(info[2])
                # 3：最高价
                high = round(float(info[3]), 2)
                # 4：最低价
                low = round(float(info[4]), 2)
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
                    hist_low = target_df.loc[index, 'low']
                    hist_high = target_df.loc[index, 'high']

                    tar_prices = str.split(alert_prices, ',') if alert_prices is not None else None
                    changes = str.split(alert_changes, ',') if alert_changes is not None and alert_changes != '' \
                        else None

                # 合约高低涨跌幅
                wave_str = '[]'
                if hist_high > hist_low > 0:
                    low_change = round((float(price) - float(hist_low)) / float(hist_low) * 100, 2)
                    high_change = round((float(price) - float(hist_high)) / float(hist_high) * 100, 2)
                    wave_str = '[' + str(round(hist_low, 0)) + ' +' + str(low_change) + '%, ' \
                               + str(round(hist_high, 0)) + ' ' + str(high_change) + '%]'
                value_per_contract = round(float(price) * amount_per_contract, 2)
                margin_per_contract = round(value_per_contract * margin_rate / 100, 2)
                try:
                    contract_num_for_1m = int(1000000 / value_per_contract) + 1
                    margin_for_1m = round(contract_num_for_1m * value_per_contract * margin_rate / 100, 2)

                    if float(price) < float(hist_low) or float(hist_low) == 0:
                        update_low_sql = "update future_basics set low=%.2f where name like '%s'" % (
                            low, '%' + alias + '%')
                        cursor.execute(update_low_sql)
                        db.commit()
                        print(name, '更新合约历史最低价成功!')
                    if float(price) > float(hist_high):
                        update_high_sql = "update future_basics set high=%.2f where name like '%s'" % (
                            high, '%' + alias + '%')
                        cursor.execute(update_high_sql)
                        db.commit()
                        print(name, '更新合约历史最高价成功!')
                except Exception as err:
                    print("  >>>error:", name, "数据有误:", info, err)
                    db.rollback()

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
                # alert_trigger(symbol=name, realtime_price=price, prices=tar_prices, realtime_change=change, changes=changes)
                notify_trigger(symbol=name, price=price, alert_prices=tar_prices, alert=True)

                row_list = [name, alias, exchange, price, change, limit_in, bid, ask, low, high,
                            round(position, 2), str(high - low) + '-' + str(round((high - low) / high * 100, 2)) + '%',
                            wave_str, margin_rate, value_per_contract, margin_per_contract,
                            str(contract_num_for_1m) + '-' + str(margin_for_1m),
                            trade_date, date_util.get_now(), low_change, high_change]
                result_list.append(row_list)
            df = pd.DataFrame(result_list, columns=['name', 'alias', 'exchange', 'price', 'change', 'limit',
                                                    'bid1', 'ask1', 'low', 'high', 'position', 'amp', 'wave',
                                                    'margin_rate',
                                                    'one_value', 'one_margin', 'onem_margin', 'date', 'time',
                                                    'low_change', 'high_change'])
            if group_type == 'd':
                df = df.sort_values(['change'], ascending=False)
            else:
                df = df.sort_values(['change'])

            db_util.to_db(df, tbname='future_realtime')

            final_df = format_realtime(df)
            if final_df.empty:
                print('no data, exit!')
                break
            print(final_df)
            # print(future_from_sina, '可查')
            if len(future_name_list) > 0:
                print(tuple(future_name_list), '查无结果!')
            time.sleep(interval)

    # 关闭游标和数据库的连接
    cursor.close()
    db.close()


def alert_trigger(symbol=None, realtime_price=None, prices=None, realtime_change=None, changes=None,
                  receive_mobile='18507550586'):
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
    if len(argv) > 1 and argv[1] in group_list:
        group = argv[1]
    else:
        group = None
    re_exe(3, group_type=group)
