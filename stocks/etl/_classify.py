import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import _datautils

# [get concept data]
concept = ts.get_concept_classified()
concept.to_csv("../data/concept.csv")

_datautils.to_db(concept, tbname='concept')