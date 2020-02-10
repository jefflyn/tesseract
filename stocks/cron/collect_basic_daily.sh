#!/usr/bin/env bash

cd $STOCKS_HOME/data/etl/basic_data
python3 ./collect_hist_trade_date.py
python3 ./collect_basics.py

echo "finished collect_basic_daily"
