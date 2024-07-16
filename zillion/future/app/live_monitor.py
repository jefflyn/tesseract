import pandas as pd

from zillion.future.app import live

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
# nohup redis-server /Users/ruian/etc/redis.conf &
init_target = {
    'SC2408': [[-450], [750]],
    'TA2409': [[-5700], [6500]],
    # 'PP2409': [[-6800], [8000]],
    'PG2409': [[-4350], [4950]],
    'EB2408': [[-9000], [10000]],
    'NR2409': [[-11200], [15000]],
    'SP2409': [[-5500], [6500]],

    # 'RM2409': [[-2400], [2626]],
    'OI2409': [[-7800], [10000]],
    'P2409': [[-7300], [8600]],
    # 'CJ2409': [[-12000], [13000]],
    'CF2409': [[-14000], [16400]],
}

holding_cost = {
    'TA2405': [-5970, 20], 'PP2405': [-7164, 0], 'EB2405': [9121, 0], 'PG2404': [4613, 0], 'NR2405': [12675, 9],
    'SP2405': [5672, 0],
    'OI2405': [7730, 10], 'P2405': [1974, 0], 'RM2405': [2500, 0], 'CJ2405': [12715, 0], 'CF2405': [15945, 0],
}

if __name__ == '__main__':
    live.show(init_target, holding_cost)
