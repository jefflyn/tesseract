import requests

from zillion.future import future_util
from zillion.utils import date_util
from zillion.utils.db_util import get_db

last_trade_date = date_util.get_previous_trade_day()
future_basics = future_util.get_future_basics()
last_trade_data = future_util.get_future_daily(trade_date=last_trade_date)
last_trade_data_names = list(last_trade_data['name'])
last_trade_data.index = last_trade_data_names

if __name__ == '__main__':
    # http://hq.sinajs.cn/list=nf_LH2109
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
            # 5：昨日收盘价（不准）
            pre_close = float(info[5])
            if name in last_trade_data_names:
                last_trade_close = last_trade_data.loc[name, 'close'] if last_trade_data.empty is False else None
                if last_trade_close is not None:
                    pre_close = float(last_trade_close)
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

            settle_diff = float(price) - float(pre_settle)
            close_diff = float(price) - float(pre_close)

            s_change = round(settle_diff / float(pre_settle) * 100, 2)
            p_change = round(close_diff / float(pre_close) * 100, 2)

            # 建立数据库连接
            db = get_db()
            # 使用cursor()方法创建一个游标对象
            cursor = db.cursor()
            try:
                cursor.execute(
                    'insert into future_daily(trade_date, name, s_change, p_change, open, close, high, low, hl_diff,'
                    'amplitude, settle, pre_close, pre_settle, deal_vol, hold_vol, exchange) '
                    'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (trade_date, name, s_change, p_change, open, price, high, low, round(high-low, 2),
                     round((high - low) / high * 100, 2), settle, pre_close, pre_settle, deal_vol, hold_vol, exchange))
                db.commit()
                print('>>> insert', name, 'success')
            except Exception as err:
                print('>>> failed!', err)
                db.rollback()
            # 关闭游标和数据库的连接
            cursor.close()
            db.close()
