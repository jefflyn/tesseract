import pandas as pd
from stocks.app import selector
from stocks.data import _datautils as _dt
from stocks.data.concept import constants as CCONTS
from stocks.data.industry import constants as ICONTS

"""
don't commit this file
"""

pd.set_option('display.width', 2000)
pd.set_option('max_columns', 50)
pd.set_option('max_rows', 300)


if __name__ == '__main__':
    # selector.select_from_all()
    # selector.select_from_subnew(fname='subnew')
    # selector.select_from_concepts(CCONTS.TSL, 'tsl')
    selector.select_from_industry(ICONTS.SPYL, 'spyl')
    # selector.select_from_result(_dt.get_ot_codes(), 'ot')
    # selector.select_from_result(_dt.get_app_codes(), 'app')
    # selector.select_from_result(_dt.get_monitor_codes('my'), 'my')







