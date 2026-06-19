from zillion.future.domain import daily, trade

if __name__ == '__main__':
    df = daily.load_latest_daily("fetch_daily_result.parquet")
    if df is not None and not df.empty:
        df_dict = df.set_index('code').to_dict(orient='index')
        print(f"Loaded {len(df_dict)} records")

        codes = list(df_dict.keys())
        realtime_df = trade.realtime(codes)
        if realtime_df is not None and not realtime_df.empty:
            gap_list = []
            for index, row in realtime_df.iterrows():
                code = row.get('code', index)
                # Access specific columns
                open_p = row.get('open', 0)
                low = row.get('low', 0)
                high = row.get('high', 0)
                pre_low = df_dict[code]['low']
                pre_high = df_dict[code]['high']
                if open_p < pre_low or high < pre_low:
                    gap_p = round((open_p - pre_low) * 100 / pre_low, 2)
                    gap_list.append([code, gap_p, pre_low   ])
                elif open_p > pre_high or low > pre_high:
                    gap_p = round((open_p - pre_high) * 100 / pre_high, 2)
                    gap_list.append([code, gap_p, pre_high])
                # Your processing logic here
            print(gap_list)

    else:
        print("No data found in daily result file")