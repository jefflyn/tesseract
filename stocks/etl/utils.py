
def basic_filter(basics, cyb = False, before = 20170701):
    # filter unused code
    if cyb is False :
        basics = basics[basics['code'].str.get(0) != '3']
    basics = basics[(basics['timeToMarket'] > 0) & (basics['timeToMarket'] <= before)]
    return basics