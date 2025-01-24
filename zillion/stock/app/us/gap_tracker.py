from utils.datetime import date_util
from zillion.stock.dao.basic_us_dao import BasicUsDAO
from zillion.stock.dao import daily_quote_dao
from zillion.stock.db_stock import db_manager


# 获取股票数据
def get_stock_data(stock_symbol, start_date, end_date):
    # stock = yf.Ticker(stock_symbol)
    # data = stock.history(start=start_date, end=end_date)
    data_df = daily.get_daily(code=stock_symbol, start_date=start_date, end_date=end_date)
    data_df = data_df.reset_index()
    return data_df


# 计算每天仍然存在的缺口
def find_existing_gaps(data):
    gaps = []
    latest = data.tail(1)
    idx = latest.index.to_numpy()[0]
    latest_price = round(latest.at[idx, 'close'], 2)
    latest_date = latest.at[idx, 'date']
    high_list = list(data['high'])
    low_list = list(data['low'])
    date_list = list(data['date'])
    for index, row in data.iterrows():
        if index == len(high_list) - 1:
            break
        current_date = row['date']
        current_low = round(low_list[index], 2)
        current_high = round(high_list[index], 2)
        # 寻找之后数据中的最高价和最低价
        # next_low = min(low_list[index + 1:])
        # next_high = max(high_list[index + 1:])
        direction = None
        gap_from = None
        gap_to = None
        gap_size = None
        is_closed = 0
        closed_date = None
        days = 0
        current_price = latest_price
        for nxt_idx in range(index + 1, len(high_list)):
            # 下一日
            next_low = round(low_list[nxt_idx], 2)
            next_high = round(high_list[nxt_idx], 2)
            # 忽略当天回补的
            if direction is None and next_low > current_high:
                direction = "向上"
                gap_from = current_high
                gap_to = next_low if gap_to is None or next_low < gap_to else gap_to
                gap_size = round((next_low - current_high) * 100 / current_high, 2)
                current_gap_size = round((current_high - latest_price) * 100 / latest_price, 2)
                days = date_util.date_diff(current_date, latest_date)
            elif direction is None and next_high < current_low:
                direction = "向下"
                gap_from = current_low
                gap_to = next_high if gap_to is None or next_high > gap_to else gap_to
                gap_size = round((next_high - current_low) * 100 / current_low, 2)
                current_gap_size = round((current_low - latest_price) * 100 / latest_price, 2)
                days = date_util.date_diff(current_date, latest_date)
            if direction is None:
                break
            if (direction == "向上" and next_low <= current_high) \
                    or (direction == "向下" and next_high >= current_low):
                is_closed = 1
                closed_date = date_list[nxt_idx]
                days = date_util.date_diff(current_date, closed_date)
                current_gap_size = 0
                break

        if direction is not None:
            data_to_insert = [(row['code'], current_date, direction, round(gap_from, 2), round(gap_to, 2), gap_size,
                               is_closed, closed_date, days, float(current_price), float(current_gap_size))]
            sql = "insert into gap_track (code, gap_date, direct, gap_from, gap_to, gap_size, closed, closed_date, " \
                  "days, curt_price, curt_gap_size) " \
                  "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            db_manager.executemany(sql, data_to_insert)
    return gaps


if __name__ == "__main__":
    codes = BasicUsDAO.get_selected_codes()
    # codes = ['BABA']
    for stock_symbol in codes:
        db_manager.execute("delete from gap_track where code='" + stock_symbol + "'")

        start_date = '2023-01-01'  # 起始日期
        end_date = date_util.get_today()  # 结束日期

        stock_data = get_stock_data(stock_symbol, start_date, end_date)
        existing_gaps = find_existing_gaps(stock_data)

        # latest = stock_data.tail(1)
        # idx = latest.index.to_numpy()[0]
        # latest_date = latest.at[idx, 'date']
        # latest_price = latest.at[idx, 'close']
        # print(f"【{stock_symbol}】缺口统计：{start_date} 至 {latest_date}, 最新价格【{latest_price}】")
        # for date, gap_direction, gap, previous_price, next_price, room in existing_gaps:
        #     print(f"日期：{date}, 缺口方向：{gap_direction}, 缺口大小：{gap:.2f}, "
        #           f"缺口价格：{previous_price:.2f}-{next_price:.2f}, 缺口空间：{room:.2%}")
        print(stock_symbol, "find_existing_gaps done!")
