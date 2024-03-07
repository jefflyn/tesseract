import pandas as pd

from zillion.future.app import live

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
# nohup redis-server /Users/ruian/etc/redis.conf &
init_target = {
    'SC2404': [[-450], [750]],
    'TA2405': [[-5500], [6500]],
    # 'PP2405': [[-6800], [8000]],
    'PG2404': [[-4680], [4800]],
    'EB2404': [[-9100], [9200]],
    # 'NR2405': [[-11535], [13000]],
    'SP2405': [[-5750], [6000]],

    # 'RM2405': [[-2400], [2626]],
    'OI2405': [[-7750], [8100]],
    # 'P2405': [[-7000], [8000]],
    'CJ2405': [[-12000], [13000]],
    'CF2405': [[-15760], [16200]],
}

holding_cost = {
    'TA2405': [5836, 20], 'PP2405': [-7164, 0], 'EB2403': [8000, 0], 'PG2403': [4350, 4], 'NR2404': [11560, 0],
    'SP2405': [5672, 4],
    'OI2405': [7730, 10], 'P2405': [1974, 0], 'RM2405': [2500, 5], 'CJ2405': [12715, 0], 'CF2405': [-16760, 0],
}

if __name__ == '__main__':
    live.show(init_target, holding_cost)
