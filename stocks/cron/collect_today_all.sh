#!/usr/bin/env bash

source ~/.bash_profile

cd $STOCKS_HOME/data/etl/basic_data
python3 ./collect_today_all.py

echo "finished collect_today_all"
