#!/usr/bin/env bash

cd $STOCKS_HOME/data/etl/trading
python3 ./collect_trade_daily.py
python3 ./collect_ma_data.py
echo "finished collect_trade_daily"
