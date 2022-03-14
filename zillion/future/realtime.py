import time
from sys import argv

import pandas as pd
import requests

from zillion.future import future_util
from zillion.future.future_constants import *
from zillion.utils import date_util
from zillion.utils import db_util
from zillion.utils import notify_util
from zillion.utils import sms_util, date_const
from zillion.utils.db_util import get_db
from zillion.utils.redis_util import redis_client

group_list = ['tar', 'all', 'ag', 'om', 'ch1', 'ch2', 'ch3', 'bk', 'en', 'pm', 'nfm', 'fi']
price_flash_key = 'PRICE_FLASH_'
# 建立数据库连接
db = get_db()
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()


def format_realtime(df):
    '''
    格式化数据
    :param df:
    :return:
    '''
    # format data
    df['low'] = df['low'].apply(lambda x: '_' + str(round(float(x), 2)))
    df['high'] = df['high'].apply(lambda x: '^' + str(round(float(x), 2)))
    df['change'] = df['change'].apply(lambda x: str(round(x, 2)) + '%')
    df['position'] = df['position'].apply(lambda x: 'p-' + str(round(x, 2)) + '%')
    df['limit'] = df['limit'].apply(lambda x: '^' + str(round(x, 2)) + '%')
    df['margin_rate'] = df['margin_rate'].apply(lambda x: str(x) + '%')
    df['per_margin'] = df['per_margin'].apply(lambda x: '[' + str(x) + ',')
    df['per_value'] = df['per_value'].apply(lambda x: str(x) + '')
    df['m_quantity'] = df['m_quantity'].apply(lambda x: str(x) + ':')
    df['m_margin'] = df['m_margin'].apply(lambda x: str(x) + ']')
    return df


def re_exe(interval=10, group_type=None, sort_by=None):
    """
    执行入口
    http://hq.sinajs.cn/list=nf_SA2101
    :param interval:
    :param group_type:
    :return:
    """
    on_target = (group_type is None or group_type == 'tar')
    while True:
        is_trade_time = future_util.is_trade_time()
        future_basics = future_util.get_future_basics(type=group_type, on_target=on_target)
        future_name_list = list(future_basics['name'])
        codes = ','.join(['nf_' + e for e in list(future_basics['symbol'])])
        req_url = 'https://hq.sinajs.cn/list='
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
                buy_vol = float(info[11])
                # 12：卖量
                sell_vol = float(info[12])
                # 13：持仓量
                hold_vol = float(info[13])
                # 14：成交量
                deal_vol = float(info[14])
                # 15：商品交易所简称
                exchange = info[15]
                # 16：品种名简称
                alias = info[16]
                # 17：日期
                trade_date = info[17]
                future_from_sina.append(alias)
                # print(info)

                # 清除可以查询的商品
                for goods_name in future_name_list:
                    if goods_name.startswith(alias):
                        future_name_list.remove(goods_name)

                if redis_client.get('PRE_PRICE_' + trade_date + name) is None:
                    redis_client.set('PRE_PRICE_' + trade_date + name, pre_close, date_const.ONE_HOUR * 12)
                else:
                    pre_close = redis_client.get('PRE_PRICE_' + trade_date + name)
                    # if (float(open) - float(pre_close)) / float(pre_close) > 0.0033:


                target_df = future_basics.loc[future_basics['name'].str.startswith(alias)]
                if target_df.empty:
                    print(name, alias, 'empty')
                for index, row in target_df.iterrows():
                    symbol_code = row['symbol']
                    amount_per_contract = row['amount']
                    limit_in = row['limit']
                    margin_rate = row['margin_std']
                    alert_on = target_df.loc[index, 'alert_on']
                    alert_prices = target_df.loc[index, 'alert_price']
                    alert_changes = target_df.loc[index, 'alert_change']
                    receive_mobile = target_df.loc[index, 'alert_mobile']
                    hist_low = target_df.loc[index, 'low']
                    hist_high = target_df.loc[index, 'high']

                    tar_prices = str.split(alert_prices, ',') if alert_prices is not None else None
                    changes = str.split(alert_changes,
                                        ',') if alert_changes is not None and alert_changes != '' else None

                price_diff = float(price) - float(pre_settle)
                change = round(price_diff / float(pre_settle) * 100, 2)
                value_per_contract = round(float(price) * amount_per_contract, 2)
                margin_per_contract = round(value_per_contract * margin_rate / 100, 2)
                contract_num_for_1m = int(1000000 / value_per_contract) + 1
                margin_for_1m = round(contract_num_for_1m * value_per_contract * margin_rate / 100, 2)

                position = 0
                if high != low:
                    position = round((price - low) / (high - low) * 100, 2)
                elif high == low > price:
                    position = 100

                wave_str = '[]'
                if hist_high > hist_low > 0:
                    low_change = round((float(price) - float(hist_low)) / float(hist_low) * 100, 2)
                    high_change = round((float(price) - float(hist_high)) / float(hist_high) * 100, 2)
                    wave_str = '[' + str(round(hist_low, 0)) + ' +' + str(low_change) + '%, ' \
                               + str(round(hist_high, 0)) + ' ' + str(high_change) + '%]'

                # ------ 提醒 -----
                if is_trade_time is not True:
                    print(date_util.get_now(), '~未开波~')
                    delete_price_flash_cached()
                else:
                    need_sms = alert_on is not None and alert_on == 1
                    high_low_flag = ''
                    if float(high) > float(hist_high) or float(hist_high) == 0:
                        high_low_flag = '^'
                    if float(low) < float(hist_low) or float(hist_low) == 0:
                        high_low_flag = '_'

                    # 价格异动触发提醒
                    trigger_price_flash(is_trade_time=is_trade_time, name=name, price=price,
                                        change=change, position=round(position), hist_new_tag=high_low_flag, alert_on=need_sms)
                    # 合约高低涨跌幅 触发提醒
                    trigger_new_high_low(name, alias, price, change, high, low, hist_high, hist_low, alert_on=need_sms)
                    trigger_price_change_msg(symbol=name, realtime_price=price, alert_prices=tar_prices,
                                             realtime_change=change, changes=changes)
                    trigger_price_notify(symbol=name, price=price, alert_prices=tar_prices, alert=need_sms)

                # 输出数据
                row_list = [name, symbol_code, exchange, price, change, limit_in, bid, ask, low, high,
                            round(position, 2),
                            str(round(high - low, 2)) + '^' + str(round((high - low) / high * 100, 2)) + '%',
                            wave_str, margin_rate, margin_per_contract, value_per_contract,
                            contract_num_for_1m, margin_for_1m,
                            date_util.get_now(),
                            low_change, high_change]
                result_list.append(row_list)
            df = pd.DataFrame(result_list, columns=['name', 'symbol', 'exchange', 'price', 'change', 'limit',
                                                    'bid1', 'ask1', 'low', 'high', 'position', 'amp', 'wave',
                                                    'margin_rate', 'per_margin', 'per_value',
                                                    'm_quantity', 'm_margin', 'time',
                                                    'low_change', 'high_change'])
            if sort_by is not None:
                if sort_by == 'd':
                    df = df.sort_values(['change'], ascending=False)
                if sort_by == 'p1':
                    df = df.sort_values(['position'])
                if sort_by == 'p2':
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
            if len(future_name_list) > 0:
                print(tuple(future_name_list), '查无结果!')
            time.sleep(interval)


def trigger_price_flash(is_trade_time=False, name=None, price=None, change=None, position=0, hist_new_tag='', alert_on=False):
    '''
    价格快速波动
    :param is_trade_time:
    :param name:
    :param price:
    :param change:
    :param alert_on:
    :return:
    '''
    key = price_flash_key + name
    secs = 50
    trigger_diff = 0.33
    redis_client.rpush(key, price)
    price_len = redis_client.llen(key)
    # [99999999|99999999] x
    steps = secs / 5
    if price_len >= steps:
        last_price = redis_client.lpop(key)
    else:
        last_price = redis_client.lindex(key, 0)
    blast_tip = ''
    if price_len > steps / 2:
        # 取FIFO队列后半价格
        late_prices = redis_client.lrange(key, int(steps / 2), price_len)
        max_price = float(max(late_prices))
        min_price = float(min(late_prices))
        diff_min = 0
        if max_price != min_price:
            diff_max = abs((price - max_price)) / max_price * 100
            diff_min = abs((price - min_price)) / min_price * 100
        else:
            diff_max = abs((price - max_price)) / max_price * 100
        if diff_max >= trigger_diff or diff_min >= trigger_diff:
            blast_tip = '￥'

    last_price = float(last_price)
    diff = abs((price - last_price)) / last_price * 100
    # print(last_price, price, diff)
    if diff >= trigger_diff or blast_tip != '':
        diff_str = str(round(diff, 2)) + '%'
        is_up = price > last_price
        suggest_price = round((last_price + price) / 2)
        position_param = str(position) + '，' + hist_new_tag + blast_tip \
                         + (LOG_TYPE_PRICE_UP if is_up else LOG_TYPE_PRICE_DOWN) + diff_str
        suggest_param = ('看多' if is_up else '看空') + str(suggest_price)

        content = str(secs) + '秒' + (blast_tip + LOG_TYPE_PRICE_UP if price > last_price
                                     else blast_tip + LOG_TYPE_PRICE_DOWN) \
            + diff_str + '【' + str(last_price) + '-' + str(price) + '】' + suggest_param
        # 添加日志
        log_type = LOG_TYPE_PRICE_UP if price > last_price else LOG_TYPE_PRICE_DOWN
        future_util.add_log(name, log_type, change, content,
                            log_type if hist_new_tag == '' or hist_new_tag is None else hist_new_tag, price, position)

        if is_trade_time and alert_on:
            if name.startswith('菜油'):
                notify_util.alert(message='起来活动一下')
        # if True:
            # 信息警告
            sms_util.send_future_msg_with_tencent(name=name, price=position_param,
                                                  suggest=suggest_param, to='18507550586')
            # print(name, suggest_price, suggest)
        # 删除价格列表，重新获取
        redis_client.delete(key)


def trigger_new_high_low(name, alias, price, change, high, low, hist_high, hist_low, alert_on):
    '''
    价格新高新低
    :param alert_on:
    :param name:
    :param alias:
    :param price:
    :param change:
    :param high:
    :param low:
    :param hist_high:
    :param hist_low:
    :return:
    '''
    try:
        msg_content = None
        update_sql = None
        log_type = ''
        # if price <= float(low):
        #     log_type = LOG_TYPE_DAY_NEW_LOW
        #     msg_content = name + '【日内】新低:' + str(low)
        #     update_sql = "update future_basics set update_remark='%s' " \
        #                  "where name like '%s'" % (msg_content, '%' + alias + '%')
        # if price >= float(high):
        #     log_type = LOG_TYPE_DAY_NEW_HIGH
        #     msg_content = name + '【日内】新高:' + str(high)
        #     update_sql = "update future_basics set update_remark='%s' " \
        #                  "where name like '%s'" % (msg_content, '%' + alias + '%')
        # ------- contract ---------
        if float(low) < float(hist_low) or float(hist_low) == 0:
            log_type = LOG_TYPE_CONTRACT_NEW_LOW
            msg_content = name + log_type + ':' + str(low)
            update_sql = "update future_basics set low=%.2f, update_remark='%s', update_time=now() " \
                         "where name like '%s'" % (low, msg_content, '%' + alias + '%')
            print('--->', name, '更新合约历史最低价!')
            if redis_client.get('CONTRACT_NEW_LOW_' + name) is not None and float(redis_client.get('CONTRACT_NEW_LOW_' + name)) >= 1:
                print("合约历史最低价提示超过限制，不再发送信息!")
            else:
                if alert_on:
                    sms_util.send_future_msg_with_tencent(code=name + log_type, name=name, price=log_type,
                                                          suggest='看空' + str(hist_low))
                    redis_client.incr('CONTRACT_NEW_LOW_' + name)
                    redis_client.expire('CONTRACT_NEW_LOW_' + name, date_const.ONE_HOUR * 4)
        if float(high) > float(hist_high) or float(hist_high) == 0:
            log_type = LOG_TYPE_CONTRACT_NEW_HIGH
            msg_content = name + log_type + ':' + str(high)
            update_sql = "update future_basics set high=%.2f, update_remark='%s', update_time=now() " \
                         "where name like '%s'" % (high, msg_content, '%' + alias + '%')
            print('--->', name, '更新合约历史最高价!')
            if redis_client.get('CONTRACT_NEW_HIGH_' + name) is not None and float(redis_client.get('CONTRACT_NEW_HIGH_' + name)) >= 1:
                print("合约历史最高价提示超过限制，不再发送信息!")
            else:
                if alert_on:
                    sms_util.send_future_msg_with_tencent(code=name + log_type, name=name, price=log_type,
                                                          suggest='看多' + str(hist_high))
                    redis_client.incr('CONTRACT_NEW_HIGH_' + name)
                    redis_client.expire('CONTRACT_NEW_HIGH_' + name, date_const.ONE_HOUR * 4)
        if msg_content is not None:
            # notify_util.alert(message=msg_content)
            # 去重
            if redis_client.exists(msg_content) is False:
                # notify_util.alert(message='起来活动一下')
                future_util.add_log(name, log_type, change, msg_content, log_type, price, None)
                redis_client.set(msg_content, str(date_util.get_now()), ex=date_const.ONE_HOUR)

        if update_sql is not None:
            cursor.execute(update_sql)
            db.commit()
    except Exception as err:
        print("  >>>error:", name, "数据有误:", err)
        db.rollback()


def trigger_price_change_msg(symbol=None, realtime_price=None, alert_prices=None, realtime_change=None, changes=None,
                             receive_mobile='18507550586'):
    '''
    短信提醒 价格、涨跌幅配置
    :param symbol:
    :param realtime_price:
    :param prices:
    :param realtime_change:
    :param changes:
    :param receive_mobile:
    :return:
    '''
    if alert_prices is not None and alert_prices != '' and len(alert_prices) > 0:
        for p in alert_prices:
            if p == '':
                continue
            target_price = round(float(p), 0)
            if 0 < target_price <= realtime_price:
                target_price = str(target_price)
                redis_key = date_util.get_today() + symbol + '_price_' + target_price
                warn_times = redis_client.get(redis_key)
                if warn_times is None:
                    try:
                        msg_content = symbol + future_util.LOG_TYPE_PRICE_ABOVE + ':' + target_price
                        future_util.add_log(symbol, future_util.LOG_TYPE_PRICE_ABOVE, realtime_change, msg_content,
                                            future_util.LOG_TYPE_PRICE_ABOVE, realtime_price, None)
                        # send msg
                        sms_util.send_future_msg_with_tencent(name=symbol, price=future_util.LOG_TYPE_PRICE_ABOVE,
                                                              suggest='看多' + target_price)
                        redis_client.set(redis_key, symbol + str(realtime_price), ex=date_const.ONE_HOUR * 4)
                    except Exception as e:
                        print(e)
            if float(target_price) < 0 and realtime_price <= abs(float(target_price)):
                target_price = str(abs(float(target_price)))
                redis_key = date_util.get_today() + symbol + '_price_' + target_price
                warn_times = redis_client.get(redis_key)
                if warn_times is None:
                    try:
                        msg_content = symbol + future_util.LOG_TYPE_PRICE_BELOW + ':' + target_price
                        future_util.add_log(symbol, future_util.LOG_TYPE_PRICE_BELOW, realtime_change, msg_content,
                                            future_util.LOG_TYPE_PRICE_BELOW, realtime_price, None)
                        # send msg
                        sms_util.send_future_msg_with_tencent(name=symbol, price=future_util.LOG_TYPE_PRICE_BELOW,
                                                              suggest='看空' + target_price)
                        redis_client.set(redis_key, symbol + str(realtime_price), ex=date_const.ONE_HOUR * 4)
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
                        name_format = '：' + symbol
                        change_str = str(round(realtime_change, 2)) + '%' if realtime_change < 0 else '+' + str(
                            round(realtime_change, 2)) + '%'
                        price_format = str(round(realtime_price)) + ' ' + change_str
                        # send msg
                        t_msg = sms_util.send_msg_with_tencent(name=name_format, price=price_format, to=receive_mobile)
                        if t_msg is not None:
                            redis_client.set(redis_key, value, ex=date_const.ONE_MONTH)
                        print(t_msg)
                    except Exception as e:
                        print(e)

            if 0 > float(p) >= realtime_change >= -20:
                if warn_times is None:
                    value = symbol + ' ' + str(realtime_price) + ' ' + str(round(realtime_change, 2)) + '%'
                    try:
                        name_format = '：' + symbol
                        change_str = str(round(realtime_change, 2)) + '%' if realtime_change < 0 else '+' + str(
                            round(realtime_change, 2)) + '%'
                        price_format = str(round(realtime_price)) + ' ' + change_str
                        # send msg
                        t_msg = sms_util.send_msg_with_tencent(name=name_format, price=price_format, to=receive_mobile)
                        if t_msg is not None:
                            redis_client.set(redis_key, value, ex=date_const.ONE_MONTH)
                        print(t_msg)
                    except Exception as e:
                        print(e)


def trigger_price_notify(symbol=None, price=None, alert_prices=None, alert=True):
    '''
    通知提示 手动设置价格
    :param alert_prices:

    :param symbol:
    :param price:
    :param alert: 是否开启弹窗
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
            # print('⚠️' + symbol + ':价格设置至少[2个]')
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


def delete_price_flash_cached():
    '''
    删除价格异动缓存
    :return:
    '''
    list_keys = redis_client.keys(price_flash_key + "*")
    for key in list_keys:
        redis_client.delete(key)


if __name__ == '__main__':
    """
    python realtime.py argv1 argv2[c|p]
    nohup /usr/local/bin/redis-server /usr/local/etc/redis.conf &
    nohup /usr/local/bin/redis-server /etc/redis.conf &
    """
    sort = None
    if len(argv) > 1 and argv[1] in group_list:
        group = argv[1]
        if len(argv) > 2:
            sort = argv[2]
    else:
        group = None
    delete_price_flash_cached()

    re_exe(3, group_type=group, sort_by=sort)
