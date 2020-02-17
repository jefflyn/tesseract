#!/usr/bin/env bash

source ~/.bash_profile

python3 $STOCKS_HOME/data/etl/basic_data/collect_fundamental_daily.py
python3 $STOCKS_HOME/data/etl/trading/collect_index_data.py
python3 $STOCKS_HOME/data/etl/trading/collect_trade_daily.py
python3 $STOCKS_HOME/cron/select_all.py
date "+%Y-%m-%d %H:%M:%S"
echo "finished all"

/Users/ruian/work/my-git/tesseract/stocks/cron/collect_basic_daily.sh
/Users/ruian/work/my-git/tesseract/stocks/cron/collect_trade_data.sh
/Users/ruian/work/my-git/tesseract/stocks/cron/collect_ma_data.sh
/Users/ruian/work/my-git/tesseract/stocks/cron/select_all.sh
/Users/ruian/work/my-git/tesseract/stocks/cron/collect_trade_weekly.sh
