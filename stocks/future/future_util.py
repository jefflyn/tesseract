from stocks.util.db_util import read_sql

#  商品类型（1=能源化工,2=黑色金属,3=贵金属,4=有色金属,5=农产品,6=金融板块）
ENERGY_CHEMICAL = '能源化工'
PRECIOUS_METAL = '贵金属'
FERROUS_METAL = '黑色金属'
NON_FERROUS_METAL = '有色金属'
AGRICULTURAL_PRODUCTS = '农产品'
FINANCIAL = '金融板块'


def get_future_basics(code=None, type=None, night=None, on_target=None):
    '''
    查询商品合约详情，不包含金融产品
    :param code:
    :param type:
    :param night:
    :param on_target:
    :return:
    '''
    sql = "select * from future_basics where 1=1 and goods_type != '金融板块' "
    if on_target is True:
        sql += 'and on_target = :on_target '
    if code is not None:
        if isinstance(code, str):
            codes = list()
            codes.append(code)
            code = codes
        sql += 'and code in :code '
    if type is not None:
        sql += 'and goods_type = :type '
    if night is not None:
        sql += 'and night = :night '
    params = {'code': code, 'type': type, 'night': night, 'on_target': 1}
    df = read_sql(sql, params=params)
    return df

