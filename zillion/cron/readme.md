00 0,2,4,6,8 * * 1-6 ps -ef | grep realtime.py | grep -v grep | awk '{print $2}' | xargs kill -9 >> ~/future.log 2>&1
00 09 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/future_realtime_start.sh >> ~/future.log 2>&1
30 09,13,16 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/collect_basic_daily.sh > ~/stocks.log 2>&1
30 16,22 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/collect_trade_data.sh >> ~/stocks.log 2>&1
30 16 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/collect_ma_data.sh >> ~/stocks.log 2>&1
50 16,17,18 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/collect_index_k_data.sh >> ~/stocks.log 2>&1
30 17 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/collect_limitup_data.sh >> ~/stocks.log 2>&1
45 17 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/select_all_report.sh >> ~/stocks.log 2>&1
10 10,21 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/collect_today_all.sh >> ~/stocks.log 2>&1
20 10,15 * * 1 /Users/ruian/work/my-git/tesseract/stocks/cron/collect_trade_weekly.sh >> ~/stocks.log 2>&1
15 15,16 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/collect_future_daily.sh >> ~/future.log 2>&1

00 09 * * 1-5 /Users/linjingu/work/machine-learning/stocks/cron/future_realtime_start.sh >> ~/future.log 2>&1
30 09,16 * * 1-5 /Users/linjingu/work/machine-learning/stocks/cron/collect_basic_daily.sh > ~/stocks.log 2>&1
30 16 * * 1-5 /Users/linjingu/work/machine-learning/stocks/cron/collect_trade_data.sh >> ~/stocks.log 2>&1
30 16 * * 1-5 /Users/linjingu/work/machine-learning/stocks/cron/collect_ma_data.sh >> ~/stocks.log 2>&1
50 16,17,18 * * 1-5 /Users/linjingu/work/machine-learning/stocks/cron/collect_index_k_data.sh >> ~/stocks.log 2>&1
45 17 * * 1-5 /Users/linjingu/work/machine-learning/stocks/cron/select_all_report.sh >> ~/stocks.log 2>&1
30 17 * * 1-5 /Users/linjingu/work/machine-learning/stocks/cron/collect_limitup_data.sh >> ~/stocks.log 2>&1
10 10,21 * * 1-5 /Users/linjingu/work/machine-learning/stocks/cron/collect_today_all.sh >> ~/stocks.log 2>&1
20 10,15 * * 1 /Users/linjingu/work/machine-learning/stocks/cron/collect_trade_weekly.sh >> ~/stocks.log 2>&1