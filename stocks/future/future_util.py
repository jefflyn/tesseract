from stocks.util.db_util import read_sql

# 商品类型
ENERGY = '能源'
CHEMICAL = '化工'
COAL = '煤炭'
PRECIOUS_METAL = '贵金属'
FERROUS_METAL = '黑色金属'
OIL_MATERIAL = '油脂油料'
NON_FERROUS_METAL = '有色金属'
AGRICULTURAL_PRODUCTS = '农产品'
FINANCIAL = '金融板块'
GOODS_TYPE_MAP = {
    'ag': AGRICULTURAL_PRODUCTS,
    'om': OIL_MATERIAL,
    'ch': CHEMICAL,
    'en': ENERGY,
    'co': COAL,
    'pm': PRECIOUS_METAL,
    'fm': FERROUS_METAL,
    'nfm': NON_FERROUS_METAL,
    'fi': FINANCIAL
}


def get_future_basics(code=None, type=None, night=None, on_target=None):
    '''
    查询商品合约详情，不包含金融产品
    :param code:
    :param type:
    :param night:
    :param on_target:
    :return:
    '''
    sql = "select * from future_basics where 1=1 and deleted = 0 and goods_type != '有色金属'"
    if on_target is True:
        sql += 'and target = :on_target '
    if code is not None:
        if isinstance(code, str):
            codes = list()
            codes.append(code)
            code = codes
        sql += 'and code in :code '
    if type is not None and type not in ['d', 'all']:
        sql += 'and goods_type = :type '
    if night is not None:
        sql += 'and night = :night '
    params = {'code': code, 'type': GOODS_TYPE_MAP.get(type), 'night': night, 'on_target': 1}
    df = read_sql(sql, params=params)
    return df

