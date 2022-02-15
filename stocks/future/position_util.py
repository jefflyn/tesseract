if __name__ == '__main__':
    price = 12011.00
    bottom = 8908.00
    top = 12916.00
    position = (price - bottom) / (top - bottom) * 100
    print(str(round(position, 2)) + '%')
