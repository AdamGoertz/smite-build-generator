import sqlite3

class SmiteDBConnection:
    DB_NAME = "../smiteuserdb.db"

    def __init__(self):
        self.conn = sqlite3.connect(SmiteDBConnection.DB_NAME)
