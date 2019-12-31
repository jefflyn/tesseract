#!/usr/bin/env bash

source ~/.bash_profile

python3 $STOCKS_HOME/app/selection/select_all.py
python3 $STOCKS_HOME/app/report/report_select.py

date "+%Y-%m-%d %H:%M:%S"
echo "finished all"
