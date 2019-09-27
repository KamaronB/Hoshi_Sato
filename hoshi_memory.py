import sqlite3
from sqlite3 import Error



class Memory:

    """Database connections and functions for hoshi"""


    def __init__(self):
        self.file_name='/home/morty/hoshi/pythonsqlite.db'
        self.connnection=self.conn(self.file_name)

    def conn(self,db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return(conn)
        except Error as e:
            print(e)



    def create_table(self,sql):
        conn=self.connnection
        try:
            c = conn.cursor()
            c.execute(sql)

        except Error as e:
            print(e)


    def insert_name(self,value):
        conn=self.connnection
        try:
            input=(value,)
            sql=''' INSERT INTO names(name)
                     VALUES(?) ; '''
            c = conn.cursor()
            c.execute(sql,input)
            conn.commit()

        except Error as e:
            print(e)


    def get_names(self):
        conn=self.connnection
        try:
            sql="SELECT * FROM names"
            c = conn.cursor()
            c.execute(sql)
            data2= c.fetchall()
            return(data2)

        except Error as e:
            print('error at get_names')
            print(e)

    ##create tables

    # create_table( """Create table if not exists Names(  id integer PRIMARY KEY,name text NOT NULL);""")
    # create_table( """Create table if not exists Commands(  id integer PRIMARY KEY,command text NOT NULL);""")
    #
    # insert_name('kamaron')
    # get_name('*')
