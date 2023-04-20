import akshare as ak
import pandas as pd

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

if __name__ == "__main__":
    # result_df = pd.DataFrame()
    # for item in {"科技类", "金融类", "医药食品类", "媒体类", "汽车能源类", "制造零售类"}:
    #     stock_us_famous_spot_em_df = ak.stock_us_famous_spot_em(symbol=item)
    #     result_df = pd.concat([result_df, stock_us_famous_spot_em_df], ignore_index=True, axis=0)
    # print(result_df)

    # stock_us_zh_spot_df = ak.stock_us_zh_spot()
    # print(stock_us_zh_spot_df)
    #
    # stock_us_zh_daily_df = ak.stock_us_zh_daily(symbol="BABA")
    # print(stock_us_zh_daily_df)

    # stock_us_hist_df = ak.stock_us_hist(symbol='105.MTP', period="daily", start_date="19700101", end_date="22220101",
    #                                     adjust="qfq")
    # print(stock_us_hist_df)

    # fu_codes = ak.stock_us_code_table_fu()
    # print(fu_codes)
    stock_us_hist_fu_df = ak.stock_us_hist_fu(symbol="210182")
    print(stock_us_hist_fu_df)
    #
    stock_us_daily_df = ak.stock_us_daily(symbol="BABA", adjust="qfq")
    print(stock_us_daily_df)
