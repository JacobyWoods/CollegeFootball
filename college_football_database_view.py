import sqlite3
import pandas as pd


def college_football_database_view():

    con = sqlite3.connect("Database/cfb.db")
    '''These are the tables in the database:
    cfb2013  cfb2014  cfb2015  cfb2016  cfb2017  cfb2018  cfb2019  cfb2020
    '''

    df = pd.read_sql_query('SELECT * FROM "cfb2020"', con)
    pd.set_option('display.max_columns', None)

    df.to_csv('Database/2020_all.csv')

    print(df.describe())

if __name__ == '__main__':

    college_football_database_view()