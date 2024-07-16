import os
import time
from datetime import datetime


def timer(func):
    '''
    # 装饰器，计算需要的时间
    :param func:
    :return:
    '''

    def decor(*args):
        start_time = time.time()
        func(*args)
        end_time = time.time()
        d_time = end_time - start_time
        print("total consume time is", d_time)

    return decor


def is_inrange(num=None, begin=None, end=None):
    """
     begin: include
     end: exclude
    """
    if num is None or begin is None:
        return False
    if end is None:
        return num >= begin
    else:
        return num >= begin and num < end


def is_halting(code, latest_date_str=None):
    starttime = datetime.now()
    latest_date = datetime.strptime(latest_date_str, '%Y-%m-%d')
    delta = starttime - latest_date
    # excluding halting
    if delta.days > 4:
        print(code + ' halting...')
        return True
    else:
        return False


def isnumber(a):
    try:
        float(a)
        return True
    except:
        return False


def chdir(path=None):
    if path is None:
        return os.getcwd()
    os.chdir(path)


if __name__ == '__main__':
    print(is_inrange(0.1, 0, 0.11))
