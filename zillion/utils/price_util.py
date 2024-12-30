import numpy as np


def isnumber(a):
    try:
        float(a)
        return True
    except:
        return False


def is_valid_price(price):
    if isnumber(price) is False or float(price) < 0:
        print('price must be numeric and not negative')
        return False
    return True


def future_price(price):
    price_str = str(price)
    price_arr = price_str.split(".")
    if len(price_arr) == 1:
        return price_arr[0]
    else:
        decimal = price_arr[1]
        if int(decimal) == 0:
            return price_arr[0]
        else:
            return price_arr[0] + '.' + decimal[0]


def format_large_number(value):
    """
    格式化数字，转为带单位的字符串，四舍五入保留整单位。
    如：398033799088 -> '3980亿'
    """
    units = ["", "万", "亿", "万亿"]  # 单位
    factor = 10000  # 每个单位之间的倍数
    unit_index = 0  # 当前单位的索引

    while abs(value) >= factor and unit_index < len(units) - 1:
        value /= factor
        unit_index += 1

    # 四舍五入后保留整数
    return f"{round(value)}{units[unit_index]}"


def format_large_number_vectorized(series):
    """
    矢量化版本的格式化函数，将大数字转换为带单位的字符串。
    """
    units = ["", "万", "亿", "万亿"]
    thresholds = [1, 10 ** 4, 10 ** 8, 10 ** 12]

    # 使用 numpy 进行处理
    series = np.array(series, dtype=np.float64)
    result = series.astype(str)  # 默认字符串表示

    for i in range(len(thresholds) - 1, 0, -1):
        mask = series >= thresholds[i]
        result[mask] = (series[mask] / thresholds[i]).round().astype(int).astype(str) + units[i]

    return result


if __name__ == '__main__':
    print(future_price("123.9"))
    print(future_price("123.09"))
    print(future_price("123.909"))
    print(future_price("123.9888889"))
