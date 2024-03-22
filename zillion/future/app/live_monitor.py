import pandas as pd

from zillion.future.app import live

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
# nohup redis-server /Users/ruian/etc/redis.conf &
init_target = {
    'SC2405': [[-450], [750]],
    'TA2405': [[-5700], [6500]],
    # 'PP2405': [[-6800], [8000]],
    'PG2405': [[-4550], [4950]],
    'EB2405': [[-9000], [9290]],
    'NR2405': [[-11900], [12500]],
    'SP2405': [[-5500], [6250]],

    # 'RM2405': [[-2400], [2626]],
    'OI2405': [[-8200], [8500]],
    'P2405': [[-8200], [8400]],
    # 'CJ2405': [[-12000], [13000]],
    'CF2405': [[-15800], [16200]],
}

holding_cost = {
    'TA2405': [-5970, 20], 'PP2405': [-7164, 0], 'EB2405': [9121, 0], 'PG2404': [4613, 0], 'NR2405': [12675, 9],
    'SP2405': [5672, 0],
    'OI2405': [7730, 10], 'P2405': [1974, 0], 'RM2405': [2500, 0], 'CJ2405': [12715, 0], 'CF2405': [15945, 0],
}

if __name__ == '__main__':
    live.show(init_target, holding_cost)
