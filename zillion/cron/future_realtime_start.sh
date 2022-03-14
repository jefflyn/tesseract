#!/usr/bin/env bash

source ~/.bash_profile

cd $STOCKS_HOME/future

echo -e "###### future realtime start @ `date`"
python3 ./realtime.py all
echo -e "###### future realtime end @ `date` \n"
