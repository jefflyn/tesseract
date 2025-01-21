import sys
from sys import argv

import pandas as pd

pd.set_option('display.width', 800)

if len(argv) < 3:
    print("Invalid args! At least 2 args like: python ma.py code y | n ...")
    sys.exit(0)
