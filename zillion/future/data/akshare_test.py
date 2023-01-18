import akshare as ak
import pandas as pd
from akshare.futures import cons

from zillion.utils import date_util

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)


def get_daily_all(date=None):
    if date is None:
        date = cons.get_latest_data_date(date_util.now())
    dce_daily = ak.get_dce_daily(date)
    czce_daily = ak.get_czce_daily(date)
    gfex_daily = ak.get_gfex_daily(date)
    ine_daily = ak.get_ine_daily(date)
    shfe_daily = ak.get_shfe_daily(date)
    all_data = pd.concat([dce_daily, czce_daily, gfex_daily, ine_daily, shfe_daily], ignore_index=True)
    print(all_data)


if __name__ == '__main__':
    get_daily_all()
    # get_dce_daily = ak.get_dce_daily(date="20230118")
    # print(get_dce_daily)

    # get_czce_daily = ak.get_czce_daily(date="20230117")
    # print(get_czce_daily)

    # get_gfex_daily = ak.get_gfex_daily(date="20230117")
    # print(get_gfex_daily)

    # get_ine_daily = ak.get_ine_daily(date="20230117")
    # print(get_ine_daily)

    # get_shfe_daily = ak.get_shfe_daily(date="20230117")
    # print(get_shfe_daily)

    # get_cffex_daily = ak.get_cffex_daily(date="20230117")
    # print(get_cffex_daily)

    # get_futures_daily