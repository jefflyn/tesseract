#!/usr/bin/env bash

#export PYTHONPATH=/Users/ruian/work/my-git/tesseract/
export PYTHONPATH=/Users/linjingu/work/my-git/tesseract/

echo -e "###### daily start @ `date`"
/opt/miniconda3/envs/myenv/bin/python /Users/linjingu/work/my-git/tesseract/zillion/future/data/collect_daily_ak.py
echo -e "###### daily end @ `date` \n"
