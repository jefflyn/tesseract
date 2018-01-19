import numpy as np
import pandas as pd

import tushare as ts


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
        items = rangestr.split('~')
        if len(items) > 1:
            rangefrom.append(items[0])
            to = items[1]
            rangeto.append(float(to[0:len(to) - 1]))
        else:
            rangefrom.append(items[0])
            rangeto.append(float(items[0]))

    forecast['range_from'] = rangefrom
    forecast['range_to'] = rangeto
    forecast = forecast.sort_values(by='range_to', ascending=False)
    return forecast

if __name__ == '__main__':
    pd.set_option('display.width', 800)
    forecast = get_forecast(2017, 4, afterdate='2017-12-01')
    print(forecast)
