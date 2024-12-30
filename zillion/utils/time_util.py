from datetime import time


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
