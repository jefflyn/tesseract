import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import _datautils

# [get concept data]
concepts = ts.get_concept_classified()
concepts.to_csv("../data/concepts.csv")

_datautils.to_db(concepts,tbname='concepts')