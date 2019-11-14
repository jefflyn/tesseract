#!/usr/bin/env bash

cd $STOCKS_HOME/data/etl/basic_data
python3 ./collect_fundamental_daily.py
echo "finished"
