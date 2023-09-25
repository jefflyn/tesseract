from zillion.stock.data import daily
from zillion.utils import date_util


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

    latest = stock_data.tail(1)
    idx = latest.index.to_numpy()[0]
    latest_price = latest.at[idx, 'close']
    high_list = list(data['high'])
    low_list = list(data['low'])
    for index, row in data.iterrows():
        if index == len(high_list) - 1:
            break
        current_low = low_list[index]
        current_high = high_list[index]
        # 寻找之后数据中的最高价和最低价
        next_low = min(low_list[index + 1:])
        next_high = max(high_list[index + 1:])

        if next_high < current_low:
            gaps.append((row['date'], "向下", current_low - next_high, current_low, next_high,
                         (current_low - latest_price) / latest_price))
        elif next_low > current_high:
            gaps.append((row['date'], "向上", next_low - current_high, current_high, next_low,
                         (current_high - latest_price) / latest_price))
    return gaps


if __name__ == "__main__":
    codes = ['SPY', 'QQQ', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'TSM', 'BABA', 'NFLX', 'AMD',
             'INTC', 'AVGO', 'QCOM']
    for stock_symbol in codes:
        start_date = '2023-03-01'  # 起始日期
        end_date = date_util.get_today()  # 结束日期

        stock_data = get_stock_data(stock_symbol, start_date, end_date)
        existing_gaps = find_existing_gaps(stock_data)
        if len(existing_gaps) == 0:
            continue
        existing_gaps.reverse()
        latest = stock_data.tail(1)
        idx = latest.index.to_numpy()[0]
        latest_date = latest.at[idx, 'date']
        latest_price = latest.at[idx, 'close']
        print(f"【{stock_symbol}】缺口统计：{start_date} 至 {latest_date}, 最新价格【{latest_price}】")
        for date, gap_direction, gap, previous_price, next_price, room in existing_gaps:
            print(f"日期：{date}, 缺口方向：{gap_direction}, 缺口大小：{gap:.2f}, "
                  f"缺口价格：{previous_price:.2f}-{next_price:.2f}, 缺口空间：{room:.2%}")
        print("")
