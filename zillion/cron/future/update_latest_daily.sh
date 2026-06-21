#!/usr/bin/env bash

export PYTHONPATH=/Users/linjingu/work/my-git/tesseract/

echo -e "###### update_latest_daily start @ `date`"
/opt/miniconda3/envs/myenv/bin/python /Users/linjingu/work/my-git/tesseract/zillion/future/app/update_latest_daily.py
echo -e "###### update_latest_daily end @ `date` \n"
