#!/usr/bin/env bash

export PYTHONPATH=/Users/ruian/work/my-git/tesseract/

echo -e "###### daily start @ `date`"
/Users/ruian/.conda/envs/tesseract/bin/python /Users/ruian/work/my-git/tesseract/zillion/future/data/collect_daily_ak.py
echo -e "###### daily end @ `date` \n"
