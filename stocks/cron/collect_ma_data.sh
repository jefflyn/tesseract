#!/usr/bin/env bash

cd $STOCKS_HOME/data/etl/trading
python3 ./collect_ma_daily.py
echo "finished collect_ma_daily"
