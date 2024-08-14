import pandas as pd

from zillion.future.app import live

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
# nohup redis-server /Users/ruian/etc/redis.conf &
init_target = {
    'FG2409': [[-1000], [1800]],
    'SA2409': [[-1300], [2500]],
    'UR2409': [[-1700], [2500]],

    'SF2409': [[-6300], [8200]],
    'I2501': [[-700], [900]],
    'JM2409': [[-1200], [2500]],
    'J2409': [[-1500], [3000]],

    'AG2412': [[-6200], [8500]],
    # 'SN2405': [[-216500], [228000]],
    # 'NI2405': [[-123000], [150000]],
    # 'AL2312': [[-17345.0], [20000]],
    'SI2411': [[-9400], [14000]],
    'LC2411': [[-74000], [117000]],

}

holding_cost = {
    'SF2405': [6524, 10], 'I2409': [700, 10], 'JM2405': [1300, 0], 'J2405': [2000, 0],
    'FG2405': [1814, 5], 'SA2405': [2015, 0], 'UR2405': [2148, 0],

    'AG2408': [5989, 0], 'AL2305': [15000, 0], 'SN2405': [200000, 0], 'NI2405': [124000, 0],
    'SI2411': [9700, 10], 'LC2411': [75900, 20]
}

if __name__ == '__main__':
    live.show(init_target, holding_cost)
