#!/usr/bin/env bash

export PYTHONPATH=/Users/linjingu/work/my-git/tesseract/

echo -e "###### open_gap_notice start @ `date`"
/opt/miniconda3/envs/myenv/bin/python /Users/linjingu/work/my-git/tesseract/zillion/future/app/open_gap_notice.py
echo -e "###### open_gap_notice end @ `date` \n"
