import time

from akshare.futures.symbol_var import symbol_varieties

from utils.datetime import date_util
from utils.datetime.date_util import FORMAT_FLAT
from utils.mail import mail_util
from zillion.future.dao.gap_dao import GapTacticsDAO
from zillion.future.domain import daily, trade
from zillion.utils.price_util import future_price

GAP_STRAT = {''  :  {'key': 'code', 'label': '合约代码'}
             }


if __name__ == '__main__':
    gap_dao = GapTacticsDAO('future_sqlite')
    gap_map = gap_dao.get_all_gap_tactics_as_map()
    df = daily.load_latest_daily("fetch_daily_result.parquet")
    if df is not None and not df.empty:
        print('sleep for 5 seconds ...')
        time.sleep(5)
        df_dict = df.set_index('code').to_dict(orient='index')
        print(f"Loaded {len(df_dict)} records")

        codes = list(df_dict.keys())
        realtime_df = trade.realtime(codes)
        if realtime_df is not None and not realtime_df.empty:
            gap_list = []
            for index, row in realtime_df.iterrows():
                code = row.get('code', index)
                symbol = symbol_varieties(code)
                # Access specific columns
                open_p = row.get('open', 0)
                low = row.get('low', 0)
                high = row.get('high', 0)
                pre_low = df_dict[code]['low']
                pre_high = df_dict[code]['high']
                if open_p < pre_low or high < pre_low:
                    gap_p = round((open_p - pre_low) * 100 / pre_low, 2)
                    gap_list.append({
                        'code': code,
                        'name': gap_map[symbol].name, 'type': gap_map[symbol].industry,
                        'gap_type': '跳空低开',
                        'gap_per': str(gap_p) + '%', 'op': '',
                        'suggest_p': future_price(pre_low)
                    })
                elif open_p > pre_high or low > pre_high:
                    gap_p = round((open_p - pre_high) * 100 / pre_high, 2)
                    gap_list.append({
                        'code': code,
                        'name': gap_map[symbol].name, 'type': gap_map[symbol].industry,
                        'gap_type': '跳空高开',
                        'gap_per': str(gap_p) + '%', 'op': '',
                        'suggest_p': future_price(pre_high)
                    })
            gap_list = [gap for gap in gap_list if abs(float(gap['gap_per'].replace('%', ''))) >= 0.5]
            # Sort by gap_per in descending order (extract numeric value from percentage string)
            gap_list.sort(key=lambda x: float(x['gap_per'].replace('%', '')), reverse=True)
            print(gap_list)

            # Define columns to display
            columns = [
                {'key': 'code', 'label': '合约代码'},
                {'key': 'name', 'label': '名称'}, {'key': 'type', 'label': '分类'},
                {'key': 'gap_type', 'label': '缺口'},
                {'key': 'gap_per', 'label': '跳空'}, {'key': 'op', 'label': '操作'},
                {'key': 'suggest_p', 'label': '建议价格'}
            ]

            # Send email
            success = mail_util.send_mobile_friendly_email(
                to_users=['jefflyn0321@qq.com'],
                subject='【' + date_util.get_today(FORMAT_FLAT) + '】Daily Open Gap Report',
                title='📊Daily Open Gap Report',
                data=gap_list,
                columns=columns
            )

            if success:
                print(f"✅ 邮件发送成功")
            else:
                print(f"❌ 邮件发送失败")

    else:
        print("No data found in daily result file")


