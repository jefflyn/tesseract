#!/usr/bin/env bash

export PYTHONPATH=/Users/ruian/work/my-git/tesseract/

echo -e "###### update gap start @ `date`"
/Users/ruian/.conda/envs/tesseract/bin/python /Users/ruian/work/my-git/tesseract/zillion/future/future_gap.py
echo -e "###### update gap end @ `date` \n"
