from akshare.futures.symbol_var import symbol_varieties

from utils.mail import mail_util
from zillion.future.dao.basic_dao import BasicDAO
from zillion.future.domain import daily, trade
from zillion.utils.price_util import future_price

if __name__ == '__main__':
    basic_dao = BasicDAO('future_sqlite')
    basic_map = basic_dao.get_all_basic_as_map()
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
                        'name': basic_map[symbol].name, 'type': basic_map[symbol].type,
                        'gap_type': '跳空低开',
                        'gap_per': str(gap_p) + '%', 'op': '',
                        'suggest_p': future_price(pre_low)
                    })
                elif open_p > pre_high or low > pre_high:
                    gap_p = round((open_p - pre_high) * 100 / pre_high, 2)
                    gap_list.append({
                        'code': code,
                        'name': basic_map[symbol].name, 'type': basic_map[symbol].type,
                        'gap_type': '跳空高开',
                        'gap_per': str(gap_p) + '%', 'op': '',
                        'suggest_p': future_price(pre_high)
                    })
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
                subject='Daily Open Gap Report',
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


