import pandas as pd

from zillion.future.app import live

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
# nohup redis-server /Users/ruian/etc/redis.conf &
init_target = {
    'SC2412': [[-450], [750]],
    'TA2501': [[-4600], [6500]],
    'PP2501': [[-6800], [8000]],
    'PG2412': [[-4350], [6000]],
    'EB2412': [[-8000], [10000]],
    'NR2501': [[-11200], [15000]],
    'SP2501': [[-5500], [6500]],

    'RM2501': [[-2000], [2626]],
    'OI2501': [[-7800], [10000]],
    'P2501': [[-7300], [10000]],
    'CJ2501': [[-9000], [13000]],
    'CF2501': [[-10000], [16400]],
}

holding_cost = {
    'TA2405': [-5970, 20], 'PP2405': [-7164, 0], 'EB2405': [9121, 0], 'PG2404': [4613, 0], 'NR2405': [12675, 9],
    'SP2405': [5672, 0],
    'OI2405': [7730, 10], 'P2405': [1974, 0], 'RM2405': [2500, 0], 'CJ2405': [12715, 0], 'CF2405': [15945, 0],
}

if __name__ == '__main__':
    live.show(init_target, holding_cost)
