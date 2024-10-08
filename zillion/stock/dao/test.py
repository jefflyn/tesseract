from zillion.db.DataSourceFactory import session_stock
from zillion.stock.dao.basic_a_dao import BasicADAO

if __name__ == '__main__':
    basic_dao = BasicADAO(session_stock)
    all = basic_dao.get_all()
    print(all)
