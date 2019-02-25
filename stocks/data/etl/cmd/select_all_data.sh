#!/usr/bin/env bash

export PYTHONPATH=/Users/linjingu/work/git-mine/machine-learning/
export STOCKS_HOME=/Users/linjingu/work/git-mine/machine-learning/stocks

/Users/linjingu/anaconda/bin/python /Users/linjingu/work/git-mine/machine-learning/stocks/data/etl/collect_basic_daily.py
/Users/linjingu/anaconda/bin/python /Users/linjingu/work/git-mine/machine-learning/stocks/app/shell/select_all.py

