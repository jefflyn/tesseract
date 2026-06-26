import time

from akshare.futures.symbol_var import symbol_varieties

from utils.datetime import date_util
from utils.datetime.date_util import FORMAT_FLAT
from utils.mail import mail_util
from zillion.future.dao.gap_dao import GapTacticsDAO
from zillion.future.domain import daily, trade
from zillion.utils.price_util import future_price

GAP_STRAT = {'': {'key': 'code', 'label': '合约代码'}
             }


def get_gap_list():
    gap_dao = GapTacticsDAO('future_sqlite')
    gap_map = gap_dao.get_all_gap_tactics_as_map()
    df = daily.load_latest_daily("fetch_daily_result.parquet")
    if df is not None and not df.empty:
        print('sleep for 8 seconds ...')
        time.sleep(8)
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
                print(code, open_p, low, high, pre_low, pre_high)
                if open_p < pre_low and high < pre_low:
                    gap_p = round((open_p - pre_low) * 100 / pre_low, 2)
                    print(code, open_p, pre_low, gap_p)
                    gap_list.append({
                        'code': code,
                        'name': gap_map[symbol].name, 'type': gap_map[symbol].industry,
                        'gap_type': '跳空低开',
                        'gap_per': str(gap_p) + '%', 'op': '',
                        'suggest_p': future_price(pre_low)
                    })
                elif open_p > pre_high and low > pre_high:
                    gap_p = round((open_p - pre_high) * 100 / pre_high, 2)
                    print(code, open_p, pre_high, gap_p)
                    gap_list.append({
                        'code': code,
                        'name': gap_map[symbol].name, 'type': gap_map[symbol].industry,
                        'gap_type': '跳空高开',
                        'gap_per': str(gap_p) + '%', 'op': '',
                        'suggest_p': future_price(pre_high)
                    })
            print(gap_list)
            return gap_list


# ... existing code ...
if __name__ == '__main__':
    gap_list = get_gap_list()
    retry_times = 0

    while (not gap_list or len(gap_list) == 0) and retry_times < 3:
        print(f"Gap list is empty, retrying... (attempt {retry_times + 1}/3)")
        time.sleep(3)
        gap_list = get_gap_list()
        retry_times += 1

    if gap_list:
        # Split gap_list into two lists based on absolute gap_per value
        significant_gaps = [gap for gap in gap_list if abs(float(gap['gap_per'].replace('%', ''))) >= 0.33]
        minor_gaps = [gap for gap in gap_list if abs(float(gap['gap_per'].replace('%', ''))) < 0.33]

        # Sort by gap_per in descending order (extract numeric value from percentage string)
        significant_gaps.sort(key=lambda x: float(x['gap_per'].replace('%', '')), reverse=True)
        minor_gaps.sort(key=lambda x: float(x['gap_per'].replace('%', '')), reverse=True)

        # Prioritize significant_gaps, fallback to minor_gaps if empty
        final_gap_list = significant_gaps if significant_gaps else minor_gaps

        if not final_gap_list:
            print("No gap data found after filtering")
        else:
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
                data=final_gap_list,
                columns=columns
            )

            if success:
                print(f"✅ 邮件发送成功")
            else:
                print(f"❌ 邮件发送失败")
    else:
        print("No gap data found after retries")

# ... existing code ...
