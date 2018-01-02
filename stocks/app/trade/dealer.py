import sqlite3
from datetime import datetime
from pandas import DataFrame
from stocks.app import _utils

defaultcommision = 5.0
commisionrate = 0.00025
transferrate = 0.00002
taxrate = 0.001

columns = "tradedate, tradetime, tradetype, code, price, share, commision, transferfee, tax, cost"
selectclause = "SELECT " + columns + " FROM trade "

def create_trade():
    conn = _utils.get_connection()
    c = _utils.get_cursor()
    # tradedate, tradetime, tradetype, code, price, share, commision, transferfee, tax, cost
    c.execute('''CREATE TABLE IF NOT EXISTS trade
       (tradedate CHAR(10)   NOT NULL,
        tradetime CHAR(8)   NOT NULL,
        tradetype CHAR(1)  NOT NULL,
        code CHAR(6)   NOT NULL,
        price DOUBLE  NOT NULL,
        share INT     NOT NULL,
        commision DOUBLE,
        transferfee DOUBLE,
        tax DOUBLE,
        cost DOUBLE);''')
    conn.commit()
    print('Table trade created successfully')

def validate(tradetype, code, price, share):
    if tradetype not in 'bs':
        print('trade type must be \'b\' or \'s\'')
        return False
    if len(str(code)) < 6 or str(code).isdecimal() == False or str(code)[0] not in '036':
        print('invalid code')
        return False
    if _utils.isnumber(price) == False or price < 1:
        print('price must be numeric and bigger than 1')
        return False
    if str(share).isdecimal() == False or share < 100:
        print('share must be numeric and bigger than 100')
        return False


def add(tradetype, code, price, share):
    if validate(tradetype=tradetype, code=code, price=price, share=share) == False:
        return False

    conn = _utils.get_connection()
    c = _utils.get_cursor()

    now = datetime.now()
    tradedate = datetime.strftime(now, '%Y-%m-%d')
    tradetime = datetime.strftime(now, '%H:%M:%S')
    commision = 0.0
    transferfee = 0.0
    cost = 0.0
    tax = 0.0

    dealamt = price * share
    commision = round(dealamt * commisionrate, 3)
    if commision < defaultcommision:
        commision = defaultcommision;
    # SH & SZ same
    transferfee = round(dealamt * transferrate, 3)
    totalamt = dealamt + commision + transferfee
    if tradetype == 'b':
        cost = round(totalamt / share, 3)
    if tradetype == 's':
        tax = round(dealamt * taxrate, 3)

    c.execute("INSERT INTO trade VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (tradedate, tradetime, tradetype, code, price, share, commision, transferfee, tax, cost))
    conn.commit()
    print('Add record to trade successfully')

def queryall():
    conn = _utils.get_connection()
    cursor = conn.execute(selectclause)
    rows = cursor.fetchall()

    dfcolumns = columns.split(",")
    dfcolumns = [s.strip() for s in dfcolumns]
    dfvalues = []
    if len(rows) > 0:
        for i in range(len(rows)):
            rec = rows[i]
            print(rec)
            dfvalues.append(rec)
    resultdf = DataFrame(data=dfvalues, columns=dfcolumns)
    return resultdf

def querybycond(code=None, tradedate=None, tradeyear=None, trademonth=None, tradetype=None):
    return
    
def update():
    conn = _utils.get_connection()
    c = _utils.get_cursor()
    c.execute("update trade set tradedate='2017-12-14',tradetime='14:48:13' where code='600958' and tradedate='2017-12-15' and tradetime='11:46:13' and tradetype='b'")
    c.execute("update trade set tradetime='10:18:06' where code='600958' and tradedate='2017-12-15' and tradetype='s'")
    c.execute("update trade set tradetime='10:23:32' where code='000018' and tradedate='2017-12-15' and tradetype='b'")
    conn.commit()
    return

if __name__ == '__main__':
    # create_trade()
    # add('s','002158',12.04,800)
    #add('b','601890',6.59,1400)
    #add('s','600958',14.94, 700)
    df = queryall()
    print(df)
    # querybycond(code='600126')
    # querybycond(tradetype='s')
    # querybycond(code='600126', tradetype='b')
