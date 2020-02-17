#!/usr/bin/env bash

source ~/.bash_profile

cd $STOCKS_HOME/data/etl/basic_data
python3 ./collect_hist_trade_date.py
python3 ./collect_basics.py

echo "  collect_basics end " && date "+%Y-%m-%d %H:%M:%S"
echo