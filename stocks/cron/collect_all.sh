#!/usr/bin/env bash

source ~/.bash_profile

python3 $STOCKS_HOME/data/etl/basic_data/collect_fundamental_daily.py
python3 $STOCKS_HOME/data/etl/trading/collect_index_data.py
python3 $STOCKS_HOME/data/etl/trading/collect_trade_daily.py
python3 $STOCKS_HOME/data/etl/trading/collect_ma_daily.py

date "+%Y-%m-%d %H:%M:%S"
echo "finished all"
