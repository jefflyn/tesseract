#!/usr/bin/env bash

python3 $STOCKS_HOME/data/etl/basic_data/collect_fundamental_daily.py
python3 $STOCKS_HOME/shell/select_all.py
echo "finished select_all"
