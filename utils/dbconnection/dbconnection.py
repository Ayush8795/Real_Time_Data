#from ipaddress import ip_address
from urllib.parse import quote_plus as urlquote
from sqlalchemy.engine import create_engine
import sqlalchemy as sa
import pandas as pd
from sqlalchemy import insert
#from sqlalchemy import SQLAlchemyError

userName = 'walsou5_trading_user'
password = 'walsou5$trad1ng'
ip_address = '173.231.203.152'
db_name = 'walsou5_trading'


engine = create_engine('mysql+pymysql://walsou5_trading_user:%s@173.231.203.152/walsou5_trading' % urlquote('walsou5$trad1ng'))


def getConnection():
    #print(engine)
    engine_new = create_engine('mysql+pymysql://walsou5_trading_user:%s@173.231.203.152/walsou5_trading' % urlquote('walsou5$trad1ng'))
    return engine_new

def getStockList(stock_table):
    #sql = 'select * from master_stock where stock_table_name ="' + stock_table + '"'
    master_stock = sa.Table("master_stock", sa.MetaData(), autoload_with=engine)
    qry = sa.select(master_stock.c.ticker_code).where(master_stock.c.stock_table_name == stock_table)
    df = pd.read_sql_query(qry, engine)
    series =df['ticker_code']
    stock_list  = series.tolist()
    #print(stock_list)
    return stock_list

def insertSplitRecord(stock_code, s_date, s_ratio):
    master_stock_split = sa.Table("master_stock_split", sa.MetaData(), autoload_with=engine)
    try:
        insert_stmt = insert(master_stock_split).values(
                ticker_code = stock_code,
                split_date = s_date,
                split_ratio = s_ratio)
        engine.execute(insert_stmt)

    except Exception as e:
            print(e)
    finally:
        return

def testConection():
    print(engine)
    df = pd.read_sql_table('master_stock', getConnection(), columns=['ticker_code'])
    #df = pd.read_sql_query(sql, getConnection())
    print(df)
    
def getNiftyData(timeFrame):
    #sql = 'select * from master_stock where stock_table_name ="' + stock_table + '"'
    niftyTable = sa.Table('price_nifty50', sa.MetaData(), autoload_with=engine)
    #print(stockTable.c)
    qry = sa.select(niftyTable.c).where(niftyTable.c.timeframe == timeFrame).order_by(niftyTable.c.stock_date_time)
    data = pd.read_sql_query(qry, engine)
    #print(data)
    return data

#testConection()
#insertSplitRecord("Stock_AAA", '2022-01-23', 5)
#print("Record inserted...")
#testConection()
#list =getStockList('stock_Z')
#print('\n In caller listis\n', list)
