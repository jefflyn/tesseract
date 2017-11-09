import tushare as ts
import numpy as np
import pandas as pd

hist = ts.get_hist_data('600126')
print(hist.head(3))

h = ts.get_h_data('600126')
print(h.head(3))

k = ts.get_k_data('600126')
print(k.head(3))