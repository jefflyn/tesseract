

def calc_position(price, low, high):
    if low == high:
        return 0
    return round((price - low) / (high - low) * 100)
