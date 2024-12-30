

def calc_position(price, low, high):
    if low == high:
        return 0
    return round((price - low) / (high - low) * 100)


def in_range(num=None, begin=None, end=None):
    """
     begin: include
     end: exclude
    """
    if num is None or begin is None:
        return False
    if end is None:
        return num >= begin
    else:
        return begin <= num < end