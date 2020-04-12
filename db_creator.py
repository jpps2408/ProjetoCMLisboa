import sqlite3
from xlsx2csv import Xlsx2csv
import pandas as pd
from ostools import *

class db_creator(object):
    def __init__(self, csvfile,chunksize,*args, **kwargs):
        self.chunksize = chunksize
        self.csvfile = csvfile
        csv_name,_ = os.path.splitext(self.csvfile)
        self.dbfile =  csv_name + ".db"
        self.connect_2db()


    def connect_2db(self):
        if not os.path.exists(self.dbfile):
            self.create_db()
        else:
            self.conn = sqlite3.connect(self.dbfile)


    def create_db(self):
        self.conn = sqlite3.connect(self.dbfile)
        for chunk in pd.read_csv(self.csvfile, chunksize=self.chunksize,sep=";",encoding='cp860'):
            chunk.columns = chunk.columns.str.replace(' ', '_') #replacing spaces with underscores for column names
            chunk.to_sql(name="a",  con=self.conn, if_exists="append")
   

    def query_db(self,query,querytuple):
        tablecursor = self.conn.cursor()
        tablecursor.execute(query,querytuple)
        data = tablecursor.fetchall()
        return data 


        pass


   