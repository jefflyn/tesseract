#!/usr/bin/env bash
#30 16 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/start_all.sh >~/stocks.log 2>&1
#30 17 * * 1-5 python3 $STOCKS_HOME/cron/select_all.py >~/stocks.log 2>&1
#50 17 * * 1-5 python3 $STOCKS_HOME/cron/select_all.py >~/stocks.log 2>&1

source ~/.bash_profile

python3 $STOCKS_HOME/data/etl/basic_data/collect_fundamental_daily.py
python3 $STOCKS_HOME/data/etl/trading/collect_index_data.py
python3 $STOCKS_HOME/data/etl/trading/collect_trade_daily.py
python3 $STOCKS_HOME/cron/select_all.py
date "+%Y-%m-%d %H:%M:%S"
echo "finished all"
