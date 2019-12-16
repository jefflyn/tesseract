#!/usr/bin/env bash

source ~/.bash_profile

python3 $STOCKS_HOME/app/select/select_all.py
date "+%Y-%m-%d %H:%M:%S"
echo "finished all"
