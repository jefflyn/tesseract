#!/usr/bin/env bash

source ~/.bash_profile

cd $STOCKS_HOME/future

echo -e "###### collect_future_daily start @ `date`"
python3 ./future_trade_daily.py
echo -e "###### collect_future_daily end @ `date` \n"
