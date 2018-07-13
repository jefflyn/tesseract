import numpy as np
import pandas as pd

import tushare as ts

from stocks.data import _datautils
from stocks.app import _utils
from stocks.base.logging import logger


def get_forecast(year=2017, season=4, excludeCyb=True, startdate=None):
    forecast = ts.forecast_data(year, season)
    if excludeCyb:
        forecast = forecast[forecast['code'].str.get(0) != '3']
    if startdate != None:
        forecast = forecast[forecast['report_date'] >= startdate]

    ranges = list(forecast['range'])

    rangefrom = []
    rangeto =[]

    for i in range(len(ranges)):
        rangestr = ranges[i]
        logger.info('forecast range: %s' %rangestr)
        if _utils.isnumber(rangestr):
            rangefrom.append(rangestr)
            rangeto.append(rangestr)
            continue
        items = rangestr.split('~')
        if len(items) > 1:
            frm = items[0]
            to = items[1]
            rangefrom.append(float(frm[0:len(frm) - 1]))
            rangeto.append(float(to[0:len(to) - 1]))
        else:
            frm_to = items[0]
            if frm_to[-1] == '%':
                frm_to = frm_to[0:len(frm_to) - 1]
                rangefrom.append(float(frm_to))
                rangeto.append(float(frm_to))
            else:
                rangefrom.append(float(frm_to))
                rangeto.append(float(frm_to))

    forecast['range_from'] = rangefrom
    forecast['range_to'] = rangeto
    forecast['range_from'] = forecast['range_from'].astype('float32')
    forecast['range_to'] = forecast['range_to'].astype('float32')
    forecast = forecast.sort_values(by='range_to', ascending=False)
    _datautils.to_db(forecast, 'profit_forecast')
    return forecast

if __name__ == '__main__':
    pd.set_option('display.width', 800)
    forecast = get_forecast(2018, 2, startdate='2018-06-01')
    logger.info(forecast)
