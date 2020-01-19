import sys
from sys import argv

import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine
import stocks.util.db_util as _dt
from stocks.gene import limitup
from stocks.gene import maup

pd.set_option('display.width', 800)

if len(argv) < 3:
    print("Invalid args! At least 2 args like: python ma.py code y | n ...")
    sys.exit(0)
