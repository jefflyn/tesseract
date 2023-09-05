import yfinance as yf


# 获取股票数据
def get_stock_data(stock_symbol, start_date, end_date):
    stock = yf.Ticker(stock_symbol)
    data = stock.history(start=start_date, end=end_date)
    return data


# 计算每天仍然存在的缺口
def find_existing_gaps(data):
    gaps = []

    for i in range(len(data) - 1):
        current_high = data['High'][i]
        current_low = data['Low'][i]

        # 寻找之后数据中的最高价和最低价
        max_high = max(data['High'][i + 1:])
        min_low = min(data['Low'][i + 1:])

        if max_high < current_low:
            gap = current_low - max_high
            gap_direction = "向下"
            gaps.append((data.index[i].strftime('%Y-%m-%d'), gap_direction, gap, current_low, max_high))
        elif min_low > current_high:
            gap = min_low - current_high
            gap_direction = "向上"
            gaps.append((data.index[i].strftime('%Y-%m-%d'), gap_direction, gap, current_high, min_low))

    return gaps


if __name__ == "__main__":
    stock_symbol = 'AAPL'  # 股票代码，你可以替换为你感兴趣的股票
    start_date = '2023-06-01'  # 起始日期
    end_date = '2023-09-01'  # 结束日期

    stock_data = get_stock_data(stock_symbol, start_date, end_date)
    existing_gaps = find_existing_gaps(stock_data)

    print("仍然存在的每日缺口：")
    for date, gap_direction, gap, previous_price, next_price in existing_gaps:
        print(
            f"日期：{date}, 缺口方向：{gap_direction}, 缺口大小：{gap:.2f}, 前一天价格：{previous_price:.2f}, 后一天价格：{next_price:.2f}")
