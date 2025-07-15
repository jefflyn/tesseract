import pandas as pd

from zillion.future.app import live

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
# nohup redis-server /Users/ruian/etc/redis.conf &
init_target = {
    'SC2506': [[-450], [750]],
    'TA2509': [[-4000], [6500]],
    'PP2509': [[-6800], [8000]],
    'PG2506': [[-4000], [6000]],
    'EB2506': [[-5000], [10000]],
    'NR2509': [[-11200], [16000]],
    'SP2509': [[-5000], [6500]],

    'RM2509': [[-2000], [3000]],
    'OI2509': [[-7800], [10000]],
    'P2509': [[-7300], [11000]],
    'CJ2509': [[-8500], [13000]],
    'CF2509': [[-10000], [16400]],
    'AP2510': [[-5000], [10000]],
}

holding_cost = {
    'TA2405': [-5970, 20], 'PP2405': [-7164, 0], 'EB2405': [9121, 0], 'PG2404': [4613, 0], 'NR2405': [12675, 9],
    'SP2405': [5672, 0],
    'OI2405': [7730, 10], 'P2405': [1974, 0], 'RM2405': [2500, 0], 'CJ2405': [12715, 0], 'CF2405': [15945, 0],
}

if __name__ == '__main__':
    live.show(init_target, holding_cost)
