import pandas as pd
from utils.dbconnection import dbconnection as db




def get_the_ticker_codes():
    connection = db.getConnection()
    query = """SELECT DISTINCT(ticker_code) AS ticker_code FROM `Future_1d` """
    dataframe = pd.read_sql_query(sql=query, con=connection)
    # print(dataframe)
    series = dataframe['ticker_code']
    stock_list = series.tolist()
    connection.dispose()
    return stock_list