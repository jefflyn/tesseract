import pandas as pd

from zillion.future.app import live

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
# nohup redis-server /Users/ruian/etc/redis.conf &
init_target = {
    'SC2404': [[-450], [750]],
    'TA2405': [[-5500], [6500]],
    # 'PP2405': [[-6800], [8000]],
    'PG2404': [[-4550], [4800]],
    'EB2404': [[-9100], [9600]],
    'NR2405': [[-11700], [12200]],
    'SP2405': [[-5500], [6100]],

    # 'RM2405': [[-2400], [2626]],
    'OI2405': [[-7908], [8300]],
    'P2405': [[-7000], [8200]],
    # 'CJ2405': [[-12000], [13000]],
    'CF2405': [[-15900], [16200]],
}

holding_cost = {
    'TA2405': [5836, 0], 'PP2405': [-7164, 0], 'EB2405': [9121, 10], 'PG2404': [4613, 0], 'NR2405': [11810, 10],
    'SP2405': [5672, 0],
    'OI2405': [7730, 10], 'P2405': [1974, 0], 'RM2405': [2500, 0], 'CJ2405': [12715, 0], 'CF2405': [15945, 0],
}

if __name__ == '__main__':
    live.show(init_target, holding_cost)
