import pandas as pd

from zillion.future.app import live

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
# nohup redis-server /Users/ruian/etc/redis.conf &
init_target = {
    'EC2506': [[-1000], [2000]],
    'PX2505': [[-6000], [8000]],
}

holding_cost = {

}

if __name__ == '__main__':
    live.show(init_target, holding_cost)
