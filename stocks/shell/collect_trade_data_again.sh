#!/usr/bin/env bash

cd $STOCKS_HOME/data/etl/trading
python3 ./collect_trade_daily_again.py
echo "finished collect_trade_daily_again"
