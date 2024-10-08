from zillion.utils.db_util import read_sql


def get_concepts(codes=None):
    """
    获取概念信息
    :param codes:
    :return:
    """
    sql = 'select code,concepts from concepts where 1=1 '
    if codes is not None:
        if isinstance(codes, str):
            code_list = list()
            code_list.append(codes)
            codes = code_list
        sql += 'and code in :code '
    params = {'code': codes}
    df = read_sql(sql, params=params)
    df.index = df['code'].astype('str').str.zfill(6)
    return df
