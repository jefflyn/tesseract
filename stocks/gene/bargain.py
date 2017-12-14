from datetime import date
import datetime

import numpy as np
import pandas as pd

import tushare as ts

def get_bottom(df = None, limit = 20):
    starttime = datetime.datetime.now()
    if df is None:
        return df
    groupdf = df.groupby("code")
    dfresult = []
    for name, group in groupdf:
        # print(name)
        # print(group)
        size = group.iloc[:, 0].size
        startfromlast = 1
        lastestrec = group.tail(startfromlast)
        idx = lastestrec.index.get_values()[0]
        status = lastestrec.at[idx, 'status']
        bottom = lastestrec.at[idx, 'begin_price'] if status == 'up' else lastestrec.at[idx, 'end_price']

        reclist = []
        while startfromlast < size:
            startfromlast += 1
            lastrec = group.tail(startfromlast)
            lastidx = lastrec.index.get_values()[0]
            laststatus = lastrec.at[lastidx, 'status']
            lastp = lastrec.at[lastidx, 'p_change']
            if abs(lastp) < limit:
                continue
            else:
                bottom = lastrec.at[lastidx, 'begin_price'] if laststatus == 'up' else lastrec.at[lastidx, 'end_price']
                break
        reclist.append(name)
        reclist.append(bottom)
        dfresult.append(reclist)

    result = pd.DataFrame(dfresult, columns=['code', 'bottom'])

    endtime = datetime.datetime.now()
    print("total time: %ds" % (endtime - starttime).seconds)
    return result

