

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


if __name__ == '__main__':
    print(future_price("123.9"))
    print(future_price("123.09"))
    print(future_price("123.909"))
    print(future_price("123.9888889"))