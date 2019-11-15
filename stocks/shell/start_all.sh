#!/usr/bin/env bash

python3 $STOCKS_HOME/data/etl/basic_data/collect_fundamental_daily.py
python3 $STOCKS_HOME/data/etl/trading/collect_index_data.py
python3 $STOCKS_HOME/data/etl/trading/collect_trade_daily.py
python3 $STOCKS_HOME/shell/select_all.py

echo "finished all"
